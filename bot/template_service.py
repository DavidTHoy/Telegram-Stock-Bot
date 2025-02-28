templates = {
    "help": """
<b>Example usages:</b> 
<b></b>
<strong>/ticker AAPL        </strong> - Gets quote for ticker
<strong>/ticker_details AAPL</strong> - Gets quote/analyst recommendations/social sentiment if available for ticker
<strong>/er AAPL            </strong> - Gets recent ER for ticker (Up to 1 month ago). If no recent ER, will get next
<strong>/ern AAPL           </strong> - Gets next ER for ticker
<strong>/info AAPL          </strong> - Gets exensive information for ticker
""",
}


class TemplateService:
    @staticmethod
    def get_template(key):
        return templates.get(key)

    @staticmethod
    def format_template(*args):
        master_kwargs = {}
        template = ''
        for obj in args:
            if obj:
                template += obj.formatted_text()
                master_kwargs.update(obj.__dict__)
        return template.format(**master_kwargs)

    @staticmethod
    def format_yahoo_statistics(stock_ticker):
        # This will get the 52 high and low, the market cap, the PE ratio, the dividend yield, and the average volume
        link = f"https://finance.yahoo.com/quote/{stock_ticker.ticker}/key-statistics"
        try:
            stock_data = stock_ticker.info
            msg = (
                f"<b>Information pulled from:</b> {link}\n"
                f"<b>Company:</b> {stock_data.get('longName', 'N/A')} (<code>{stock_data.get('symbol', 'N/A')}</code>)\n"
                f"<b>Current Price:</b> ${stock_data.get('currentPrice', 'N/A')} <i>(Prev Close: ${stock_data.get('previousClose', 'N/A')})</i> "
                f"Percent Change: {stock_data.get('regularMarketChangePercent', 0):.2f}%\n"
                f"<b>Sector:</b> {stock_data.get('sector', 'N/A')}, <b>Industry:</b> {stock_data.get('industry', 'N/A')}\n"
                f"<b>Market Cap:</b> ${stock_data.get('marketCap', 0):,}\n"
                f"<b>Day Range:</b> ${stock_data.get('dayLow', 'N/A')} - ${stock_data.get('dayHigh', 'N/A')}\n"
                f"<b>52-Week Range:</b> ${stock_data.get('fiftyTwoWeekLow', 'N/A')} - ${stock_data.get('fiftyTwoWeekHigh', 'N/A')}\n"
                f"<b>P/E Ratio (Trailing/Forward):</b> {stock_data.get('trailingPE', 'N/A')} / {stock_data.get('forwardPE', 'N/A')}\n"
                f"<b>Profit Margin:</b> {stock_data.get('profitMargins', 0) * 100:.2f}%\n"
                f"<b>Earnings Growth:</b> {stock_data.get('earningsGrowth', 0) * 100:.2f}%\n"
                f"<b>Revenue Growth:</b> {stock_data.get('revenueGrowth', 0) * 100:.2f}%\n"
                f"<b>Return on Assets:</b> {stock_data.get('returnOnAssets', 0) * 100:.2f}%\n"
                f"<b>Return on Equity:</b> {stock_data.get('returnOnEquity', 0) * 100:.2f}%\n"
                f"<b>Total Revenue:</b> ${stock_data.get('totalRevenue', 0):,}\n"
                f"<b>Net Income:</b> ${stock_data.get('netIncomeToCommon', 0):,}\n"
                f"<b>EBITDA:</b> ${stock_data.get('ebitda', 0):,}\n"
                f"<b>Total Debt:</b> ${stock_data.get('totalDebt', 0):,}\n"
                f"<b>Free Cash Flow:</b> ${stock_data.get('freeCashflow', 0):,}\n"
                f"<b>Operating Cash Flow:</b> ${stock_data.get('operatingCashflow', 0):,}\n"
                f"<b>Institutional Holdings:</b> {stock_data.get('heldPercentInstitutions', 0) * 100:.2f}%\n"
                f"<b>Insider Holdings:</b> {stock_data.get('heldPercentInsiders', 0) * 100:.2f}%\n"
                f"<b>Short Interest Ratio:</b> {stock_data.get('shortRatio', 'N/A')}\n"
                f"<b>Short % of Float:</b> {stock_data.get('shortPercentOfFloat', 0) * 100:.2f}%\n"
                f"<b>Shares Short:</b> {stock_data.get('sharesShort', 0):,}\n"
                f"<b>Analyst Recommendation:</b> <code>{stock_data.get('recommendationKey', 'N/A').capitalize()}</code>\n"
                f"<b>Target Mean Price:</b> ${stock_data.get('targetMeanPrice', 'N/A')}\n"
                f"<b>Target High Price:</b> ${stock_data.get('targetHighPrice', 'N/A')}\n"
                f"<strong>Target Low Price:</strong> ${stock_data.get('targetLowPrice', 'N/A')}\n\n"
            )

            msg += "<b><u>News:</u></b>\n"
            for news in stock_ticker.news:
                msg += f'<a href="{news.get("content", {}).get("canonicalUrl", {}).get("url")}">{news.get("content", {}).get("title")}</a>\n'

            return msg
        except Exception as e:
            return f"Error retrieving statistics for {stock_ticker.ticker} from Yahoo -  Error: {e}"

