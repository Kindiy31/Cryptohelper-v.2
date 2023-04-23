import coinmarketcap
dbase_markets = 'markets'
is_active = 'is_active'
dbase_users = 'users'
dbase_tokens = 'tokens'

class ua_language:
    def __init__(self):
        self.name = 'Українська'
        self.coinmarket = 'CoinMarketCap'
    def markets(self):
        return 'Біржі 🏦'

    def wallet(self):
        return 'Мій гаманець 💼'

    def tokens(self):
        return 'Торгові пари 🔁'

    def tickers(self):
        return 'Токени 🪙'

    def messages(self):
        return 'Повідомлення ✍️'

    def start_msg(self):
        return '🏠 Вітаю в головному меню'

    def markets_msg(self):
        return f'🏦 Ось які біржі в даний момент ми використовуємо.\n\n' \
               f'📈Ви можете вимкнути та увімкнути біржу, в результаті чого ви отримуватимите ціни зайшовши в меню {self.tokens()}'

    def tokens_msg(self):
        return '🪙 Оберіть валюту, ціну якої бажаєте дізнатись'

    def add_token(self):
        return 'Додати пару ➕'

    def remove_token(self):
        return 'Видалити пару 🗑'

    def back(self):
        return '⬅️Назад'

    def insert_pair(self):
        return '''➕ Якщо Ви бажаєте додати валютну пару - напишіть її у форматі token_1/token_2.
        
Наприклад: BTC/USDT, ETH/USDT, USDT/UAH тощо.'''

    def pair_append(self, name):
        return f'Пару {name} успішно додано ✅'

    def error_format(self):
        return 'Введено не вірний формат ‼️'

    def token_remove_approved(self):
        return 'Пару успішно видалено 🗑'

    def set_price(self):
        return 'Встановити ціну 🫰'

    def how_price(self, price_now):
        return f'🗣 При якій ціні вас повідомити?\n\n📈 Ціна зараз: {next(iter(price_now.values()))}'

    def error(self):
        return 'Хмм... Виникла дивна помилка ‼️'

    def we_send_you(self, name, price):
        return f'🗣 Можете відпочивати, я повідомлю Вас коли ціна у парі {name} буде {price}!'

    def price_changed(self, name, price):
        return f'👋 Привіт! Я надіюсь ви добре відпочили, за цей час ціна у парі {name} досягла {price}!'

    def no_wallet(self):
        return '💼 У вас ще немає гаманця, якщо бажаєте додати - введіть вашу адресу'

    def new_address(self, address):
        return f'Ваш гаманець із адресою {address} успішно додано! 🙋'

    def your_wallet(self, address, balance, equivalents):
        msg = f'''💼  Ваш гаманець: `{address}`

💳 Баланс ETH: `{balance}`

'''
        for equivalent in equivalents:
            ticker = next(iter(equivalent.keys()))
            msg += f'''📈 Ціна за 1 ETH: `{equivalent.get(ticker).get('price')}` {ticker}
💳 Еквівалент {ticker}: `{equivalent.get(ticker).get('equivalent')}`

'''
        return msg

    def new_transaction(self, check_hash, address):
        hash = check_hash.get('hash')
        block_number = check_hash.get('blockNumber')
        from_address = check_hash.get('from')
        to_address = check_hash.get('to')
        amount = int(check_hash.get('value')) / 10 ** 18
        fee = int(check_hash.get('gas')) / 10 ** 18
        if address == from_address:
            type = '⬇️Вивід'
        else:
            type = '⬆️Поповнення'
        msg = f'''🗣 У вас нова транзакція у гаманці з адресою `{address}`!

📜 Хеш: `{hash}`
💰 Сума: `{amount} ETH`
🫰 Комісія: `{fee} ETH`
🗄 Номер блоку: `{block_number}`
🙋‍♂️ Відправник: `{from_address}`
🧏‍♂️ Отримувач: `{to_address}`
👀 Тип: {type}
'''
        return msg
    def messages_msg(self):
        return '''🗣 В даному розділі ви зможете увімкнути та виммкнути функцію сповіщення про нові транзакції у вашому гаманці.
        
Увага‼️ Сповіщення приходитимуть лише якщо вірно вказано гаманець та увімкнена ця функція❗️'''

    def on(self):
        return 'Увімкнено'

    def off(self):
        return 'Вимкнено'

    def add_ticker(self):
        return '➕ Додати валюту'

    def ticker_remove_approved(self):
        return '🗑 Валюту успішно видалено'

    def tickers_msg(self):
        return f'👨‍🎓 Тут Ви можете отримати інформацію на ваші валюти з {self.coinmarket}'

    def insert_ticker(self):
        return 'Введіть символ валюти, наприклад: BTC, ETH, USDT тощо.'

    def ticker_append(self, name):
        return f'Валюту {name} успішно додано ✅'

    def ticker_denided(self):
        return 'Валюту не знайдено 💁‍♂️'

    def ticker_info(self, info):
        msg = f'''[{info.get('name')}]({coinmarketcap.view_url}{info.get('symbol')})

*🏧 Символ*: {info.get('symbol')}
*🗄 ID {self.coinmarket}*: {info.get('id')}
*🥇 Ранг {self.coinmarket}*: {info.get('rank')}
*📝 Дата створення*: {info.get('first_historical_data')}'''
        return msg

    def remove_ticker(self):
        return 'Видалити валюту 🗑'

    def change_wallet(self):
        return 'Змінити адресу 🔁'

    def insert_new_wallet(self):
        return 'Введіть нову адресу 🖋'

    def wallet_updated(self):
        return 'Адресу успішно змінено ✅'
ua = ua_language()