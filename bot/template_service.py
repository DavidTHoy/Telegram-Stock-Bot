templates = {
    "help": """
<b>Example usages:</b> 
<b></b>
<pre>/ticker AAPL        </pre> - Gets quote for ticker
<pre>/ticker_details AAPL</pre> - Gets quote/analyst recommendations/social sentiment if available for ticker
<pre>/er AAPL            </pre> - Gets recent ER for ticker (Up to 1 month ago). If no recent ER, will get next
<pre>/ern AAPL           </pre> - Gets next ER for ticker
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
