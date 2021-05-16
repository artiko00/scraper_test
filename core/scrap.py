import json

import requests
from bs4 import BeautifulSoup

class Spider():
    def __init__(self,url):
        self.url = url
    
    def handle(self, *args, **options):
        response = requests.get(self.url)

        soup = BeautifulSoup(response.content, 'html.parser')
        script = soup.find('script', {'id': '__NEXT_DATA__'})
        json_object = json.loads(script.contents[0])

        rate = 0
        for currency in json_object['props']['initialState']['cex']['exchangeCurrencies']:
            if currency['iso'] == 'CLP':
                rate = float(currency['rate'])
                break

        open_price = float(json_object['props']['initialProps']['pageProps']['priceData']['ohlc']['open'])
        high = float(json_object['props']['initialProps']['pageProps']['priceData']['ohlc']['high'])
        low = float(json_object['props']['initialProps']['pageProps']['priceData']['ohlc']['low'])
        close = float(json_object['props']['initialProps']['pageProps']['priceData']['ohlc']['close'])

        return_ytd = soup.find('div', {'class': 'percent-change-medium'})
        return_ytd = return_ytd.find('span', {'class': 'percent-value-text'})
        return_ytd = float(return_ytd.contents[0].replace('%', ''))

        returns24 = soup.find('span', {'class': 'percent-value-text'})
        returns24 = float(returns24.contents[0].replace('%', ''))

        if rate:
            return {
            "open_price":open_price*rate,
            "high":high*rate,
            "low":low*rate,
            "volatility":close*rate,
            "return_ytd":return_ytd,
            "returns24":returns24
            }
            