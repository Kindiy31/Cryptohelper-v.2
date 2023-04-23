import requests
from data import coinmarket_api

base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": coinmarket_api
}
view_url = 'https://coinmarketcap.com/uk/currencies/'

def get_info(ticker=None):
    path = 'map'
    complete_url = base_url + path

    response = requests.get(complete_url, headers=headers)
    response = response.json()
    response = response.get('data')
    if ticker:
        info = list(filter(lambda x: x.get('symbol') == ticker, response))
        if info:
            return info[0]
    else:
        return response
