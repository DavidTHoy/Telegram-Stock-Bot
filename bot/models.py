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


class Quote:
    def __init__(self, **kwargs):
        self.current_price = kwargs.get('c')
        self.change = kwargs.get('d')
        self.percent_change = kwargs.get('dp')
        self.day_high = kwargs.get('h')
        self.day_low = kwargs.get('l')
        self.open = kwargs.get('o')
        self.previous_close = kwargs.get('pc')


class Earning:
    def __init__(self, **kwargs):
        self.date = kwargs.get('date')
        self.eps_actual = kwargs.get('epsActual')
        self.eps_estimate = kwargs.get('epsEstimate')
        self.year = kwargs.get('year')