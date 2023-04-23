from data import ether_api
import requests

base_url = 'https://api.etherscan.io/api'
def get_balance_for_address(address):

    params = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest',
        'apikey': ether_api
    }

    response = requests.get(base_url, params=params)

    # Перевіряємо код статусу відповіді
    if response.status_code == 200:
        # Отримуємо баланс
        print(response.json())
        balance = int(response.json()['result']) / 10 ** 18
        return balance

def take_last_transaction(address):
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': '0',
        'endblock': '9999999999',
        'sort': 'desc',
        'apikey': ether_api,
    }

    response = requests.get(base_url, params=params)
    response = (response.json())
    if response:
        result = response.get('result')
        if result:
            last_transaction = result[0]
            return last_transaction
