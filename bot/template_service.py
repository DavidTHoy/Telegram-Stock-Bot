template_html_map = {
    'base': """
<b>{name} ({ticker})</b>
<b></b> """,
    'quote': """
<pre>Current Price: ${current_price}</pre>
<pre>Percent Change: {percent_change}%</pre>
<pre>Open: ${open}</pre>
<pre>Previous Close: ${previous_close}</pre>
""",
    'earnings': """
<pre>EPS Actual: {eps_actual}</pre>
<pre>EPS Est: {eps_estimate}</pre>
<pre>ER Date: {date}</pre>
""",
    "help": """
<b>Example usages:</b> 
<b></b>
<pre>/ticker AAPL</pre> - Gets quote for ticker
<pre>/er AAPL</pre>     - Gets recent ER for ticker (Up to 1 month ago). If no recent ER, will get next
<pre>/ern AAPL</pre>    - Gets next ER for ticker
""",
}

template_to_html_map = {
    'base': ['base'],
    'help': ['help'],
    'quote': ['base', 'quote'],
    'earnings': ['base', 'earnings'],
    'not_found': ['base', 'not_found']
}


class TemplateService:
    @staticmethod
    def build_template(key):
        template_string = ''
        for el in template_to_html_map.get(key):
            template_string += template_html_map.get(el)
        return template_string

    @staticmethod
    def format_quote_template(template, company_obj, quote_obj):
        return template.format(**company_obj.__dict__, **quote_obj.__dict__)

    @staticmethod
    def format_earnings_template(template, company_obj, earn_obj):
        return template.format(**company_obj.__dict__, **earn_obj.__dict__)
