class CompanyProfile:
    def __init__(self, **kwargs):
        self.ticker = kwargs.get('ticker')
        self.market_cap = kwargs.get('marketCapitalization')
        self.name = kwargs.get('name')
        self.ipo = kwargs.get('ipo')
        self.outstanding_shares = kwargs.get('shareOutstanding')

    def is_real(self):
        if self.name:
            return True
        return False

    def formatted_text(self):
        return f"""
<b>{self.name} ({self.ticker})</b>
<b></b> """


class Quote:
    def __init__(self, **kwargs):
        self.current_price = kwargs.get('c')
        self.change = kwargs.get('d')
        self.percent_change = kwargs.get('dp')
        self.day_high = kwargs.get('h')
        self.day_low = kwargs.get('l')
        self.open = kwargs.get('o')
        self.previous_close = kwargs.get('pc')

    def get_change(self):
        if self.change > 0:
            return f'+${abs(self.change)}'
        return f'-${abs(self.change)}'

    def get_percent_change(self):
        if self.percent_change > 0:
            return f'+{self.percent_change}%'
        return f'{self.percent_change}%'

    def formatted_text(self):
        return f"""
<pre>Last Price: ${self.current_price}  {self.get_change()}  {self.get_percent_change()}</pre>
<pre>Open: ${self.open}</pre>
<pre>Previous Close: ${self.previous_close}</pre>
"""


class Earning:
    def __init__(self, **kwargs):
        self.date = kwargs.get('date')
        self.eps_actual = kwargs.get('epsActual')
        self.eps_estimate = kwargs.get('epsEstimate')
        self.year = kwargs.get('year')

    def formatted_text(self):
        return f"""
<pre>EPS Actual: {self.eps_actual}</pre>
<pre>EPS Est: {self.eps_estimate}</pre>
<pre>ER Date: {self.date}</pre>
"""


class Recommendation:
    def __init__(self, **kwargs):
        self.buy = kwargs.get('buy')
        self.hold = kwargs.get('hold')
        self.period = kwargs.get('period')
        self.sell = kwargs.get('sell')
        self.strong_buy = kwargs.get('strongBuy')
        self.strong_sell = kwargs.get('strongSell')

    def formatted_text(self):
        return f"""
<pre>Analyst recommendations ({self.period}): \nBUY: {self.buy} SELL: {self.sell} HOLD: {self.hold}</pre>
"""


class Sentiment:
    def __init__(self, sentiment_json):
        self.sentiment_json = sentiment_json

    def get_social_sentiment(self):
        sentiment_str = ''
        for k, v in self.sentiment_json.items():
            sentiment_str += f'{k.title()}: {Sentiment.get_readable_sentiment(v.get("total_score"))} ' \
                             f'({v.get("mentions")})\n'
        return sentiment_str

    def formatted_text(self):
        return f"""
<b>Social Sentiment for 24 hour period:</b>
<pre>{self.get_social_sentiment()}</pre>
"""

    @staticmethod
    def get_readable_sentiment(val):
        if val == 0:
            return 'Neutral'
        elif 0 < val <= 0.5:
            return 'Positive'
        elif 0.5 < val <= 1:
            return 'Very Positive'
        elif 0 > val > -0.5:
            return 'Negative'
        else:
            return 'Very Negative'
