import finnhub
from models import CompanyProfile, Quote, Earning, Recommendation, Sentiment
from settings import FINNHUB_API_KEY
from datetime import datetime
from dateutil.relativedelta import relativedelta

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


class FinnService:

    @staticmethod
    def get_all_info(ticker) -> (CompanyProfile, Quote, Recommendation):
        return FinnService.get_company_profile(ticker), FinnService.get_quote(ticker), FinnService.get_recommendation(
            ticker)

    @staticmethod
    def get_ticker_quote(ticker) -> (CompanyProfile, Quote):
        return FinnService.get_company_profile(ticker), FinnService.get_quote(ticker)

    @staticmethod
    def get_sentiment(ticker):
        now = datetime.now()
        previous_day = now - relativedelta(days=-1)
        r = finnhub_client.stock_social_sentiment(ticker, now.strftime("%Y-%m-%d"), previous_day.strftime("%Y-%m-%d"))
        day_range_sentiment = {}
        is_sentiment = False
        for k in r:
            if k == 'symbol':
                continue
            day_range_sentiment[k] = {'total_score': 0, 'mentions': 0}
            if len(r.get(k)) > 0:
                is_sentiment = True
            for v in r.get(k):
                day_range_sentiment[k]['total_score'] += v.get('score')
                day_range_sentiment[k]['mentions'] += v.get('mention')

            if day_range_sentiment[k]['total_score'] != 0:
                day_range_sentiment[k]['total_score'] = day_range_sentiment[k]['total_score'] / len(r.get(k))

        if not is_sentiment:
            return None
        return Sentiment(day_range_sentiment)

    @staticmethod
    def get_company_profile(ticker):
        return CompanyProfile(**finnhub_client.company_profile2(symbol=ticker))

    @staticmethod
    def get_quote(ticker):
        return Quote(**finnhub_client.quote(ticker))

    @staticmethod
    def get_recommendation(ticker):
        reco = finnhub_client.recommendation_trends(ticker)
        if reco:
            return Recommendation(**reco[0])
        return None

    @staticmethod
    def get_next_earnings(ticker):
        now = datetime.now()
        six_months_from_now = now + relativedelta(months=+6)
        earnings = FinnService.get_earnings(now, six_months_from_now, ticker)
        if earnings:
            return Earning(**earnings[-1])
        return None

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
