import finnhub
from models import CompanyProfile, Quote, Earning
from settings import FINNHUB_API_KEY
from datetime import datetime
from dateutil.relativedelta import relativedelta

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


class FinnService:

    @staticmethod
    def get_all_info(ticker) -> (CompanyProfile, Quote):
        return FinnService.get_company_profile(ticker), FinnService.get_quote(ticker)

    @staticmethod
    def get_company_profile(ticker):
        return CompanyProfile(**finnhub_client.company_profile2(symbol=ticker))

    @staticmethod
    def get_quote(ticker):
        return Quote(**finnhub_client.quote(ticker))

    @staticmethod
    def get_next_earnings(ticker):
        now = datetime.now()
        six_months_from_now = now + relativedelta(months=+6)
        earnings = FinnService.get_earnings(now, six_months_from_now, ticker)
        return Earning(**earnings[-1])

    @staticmethod
    def get_recent_earnings(ticker):
        now = datetime.now()
        one_month_back = now - relativedelta(months=+1)
        earnings = FinnService.get_earnings(one_month_back, now, ticker)
        if earnings:
            return Earning(**earnings[0])
        return None

    @staticmethod
    def get_earnings(start, end, ticker):
        return finnhub_client.earnings_calendar(_from=start.strftime("%Y-%m-%d"),
                                                to=end.strftime("%Y-%m-%d"),
                                                symbol=ticker, international=False).get('earningsCalendar', [])
