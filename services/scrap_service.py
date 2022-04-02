import requests

class ScrapService():
    URL_TEMPLATE = 'https://s.kubsau.ru/?type_schedule=1&val={}'

    def scrap_page(group_name: str) -> str:
        try:
            return requests.get(ScrapService.URL_TEMPLATE.format(group_name), verify=False).text
        except:
            return ''
