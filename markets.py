import requests
import json
from binance.client import Client
import texts



class whitebit:
    def __init__(self):
        self.name = 'WhiteBit'
        self.base_url = 'https://whitebit.com'

    def take_price_for_pair(self, ticker_1, ticker_2):
        response = False
        #change = None
        head_ticker = ticker_1
        request = '/api/v4/public/ticker'
        complete_url = self.base_url + request
        resp = requests.get(complete_url)
        # receiving data
        response_market = resp.json()
        #response_view = (json.dumps(resp.json(), sort_keys=True, indent=4))
        pair = f'{ticker_1}_{ticker_2}'
        info_pair = response_market.get(pair)
        if info_pair:
            #change = info_pair.get('change')
            price = info_pair.get('last_price')
            response = {head_ticker: price}

        else:
            head_ticker = ticker_2
            pair = f'{ticker_2}_{ticker_1}'
            info_pair = response_market.get(pair)
            if info_pair:
                #change = info_pair.get('change')
                price = info_pair.get('last_price')
                response = {head_ticker: price}

        return response


class binance_:
    def __init__(self):
        self.name = 'Binance'
        self.client = Client()
    def take_price_for_pair(self, ticker_1, ticker_2):
        response = False
        pairs = self.client.get_all_tickers()
        pair_name_1 = f'{ticker_1}{ticker_2}'
        pair_name_2 = f'{ticker_2}{ticker_1}'
        pairs = list(filter(lambda x: x.get('symbol') == pair_name_1 or x.get('symbol') == pair_name_2, pairs))
        if pairs:
            pairs = pairs[0]
            symbol = pairs.get('symbol')
            price = pairs.get('price')
            if symbol == pair_name_1:
                head_ticker = ticker_1
            else:
                head_ticker = ticker_2
            response = {head_ticker: price}
        return response

class KuCoin:
    def __init__(self):
        self.name = 'KuCoin'
        self.base_url = 'https://api.kucoin.com'
    def take_price_for_pair(self, ticker_1, ticker_2):
        response = False
        request = '/api/v1/market/allTickers'
        complete_url = self.base_url + request
        resp = requests.get(complete_url)
        pairs = resp.json().get('data').get('ticker')
        pair_name_1 = f'{ticker_1}-{ticker_2}'
        pair_name_2 = f'{ticker_2}-{ticker_1}'
        pairs = list(filter(lambda x: x.get('symbol') == pair_name_1 or x.get('symbol') == pair_name_2, pairs))
        if pairs:
            pairs = pairs[0]
            symbol = pairs.get('symbol')
            price = pairs.get('buy')
            if symbol == pair_name_1:
                head_ticker = ticker_1
            else:
                head_ticker = ticker_2
            response = {head_ticker: price}
        return response

def take_price_for_pair(ticker_1, ticker_2, one_price=False):
    from database import dbase
    result = False
    markets_list = list(filter(lambda x: x.get(texts.is_active), dbase.take_markets()))
    markets = []
    for market in markets_list:
        ID = market.get("ID")
        if ID == 1:
            markets.append(binance_())
        elif ID == 2:
            markets.append(whitebit())
        elif ID == 3:
            markets.append(KuCoin())
    if not markets:
        return f'Всі біржі відключеня на даний момент'
    msg = f'Торгова пара {ticker_1}/{ticker_2}.\n\nЦіни на біржах:\n'
    for market in markets:
        name = market.name
        response = market.take_price_for_pair(ticker_1=ticker_1, ticker_2=ticker_2)
        if response:
            if one_price:
                result = response
                break
            if ticker_1 in response:
                head_ticker = ticker_1
                other_ticker = ticker_2
            else:
                head_ticker = ticker_2
                other_ticker = ticker_1

            msg_dop = f'''\n{name}
1 {head_ticker} = {response.get(head_ticker)} {other_ticker}\n'''
            msg += msg_dop
        else:
            msg_dop = f'''\n{name}
❌ Пару не знайдено\n'''
            msg += msg_dop
    if one_price:
        return result
    return msg

#response = KuCoin().take_price_for_pair('USDT', 'MATIC')
#response = binance().take_price_for_pair('USDT', 'MATIC')
#response = whitebit().take_price_for_pair('USDT', 'MATIC')
#print(response)