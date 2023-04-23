from texts import ua
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import dbase
lang = ua

class keyboards_:
    def __init__(self):
        self.name = 'Кнопки'

    def generate_reply_markup(self, buttons):
        markup = types.ReplyKeyboardMarkup(selective=False, resize_keyboard=True)
        for row in buttons:
            if row:
                if len(row) != 1:
                    markup.add(*row)
                else:
                    markup.add(row[0])

        return markup

    def generate_inline_markup(self, buttons):
        markup = types.InlineKeyboardMarkup()
        for data in buttons:
            row = []
            for button in data:
                name = button.get('name')
                if 'callback' in button:
                    callback = button.get('callback')
                    row.append(types.InlineKeyboardButton(name, callback_data=callback))
                elif 'webapp' in button:
                    webapp = button.get('webapp')
                    row.append(types.InlineKeyboardButton(name, web_app=webapp))
                elif 'url' in button:
                    url = button.get('url')
                    row.append(types.InlineKeyboardButton(name, url=url))
            if row:

                if len(row) != 1:
                    markup.add(*row)
                else:
                    markup.add(row[0])
        return markup

    def home_kb(self):
        buttons = [
            [
                lang.markets(),
                lang.tokens()
            ],
            [
                lang.wallet(),
                lang.tickers()
            ],
            [
                lang.messages()
            ]
        ]
        markup = self.generate_reply_markup(buttons=buttons)
        return markup

    def markets_kb(self):
        markets = dbase.take_markets()
        buttons = []
        for market in markets:
            name = market.get('name')
            is_active = market.get('is_active')
            if is_active:
                name = f'✅ {name}'
            else:
                name = f'❌ {name}'
            buttons.append(
                [
                    {
                        'name': name,
                        'callback': f'market_change_{market.get("ID")}'
                    },
                ]
            )
        markup = self.generate_inline_markup(buttons=buttons)
        return markup

    def tokens_kb(self):
        tokens = dbase.take_tokens()
        buttons = []
        temp_list = []
        for count, token in enumerate(tokens, start=1):
            temp_list.append(token.get('name'))
            if count % 3 == 0:
                buttons.append(temp_list.copy())
                temp_list.clear()
        if temp_list:
            buttons.append(temp_list)
        buttons.append(
            [
                lang.add_token(),
            ]
        )
        buttons.append(
            [
                lang.back(),
            ]
        )
        markup = self.generate_reply_markup(buttons=buttons)
        return markup

    def tickers_kb(self):
        tickers = dbase.take_tickers()
        buttons = []
        temp_list = []
        for count, ticker in enumerate(tickers, start=1):
            temp_list.append(ticker.get('name'))
            if count % 3 == 0:
                buttons.append(temp_list.copy())
                temp_list.clear()
        if temp_list:
            buttons.append(temp_list)
        buttons.append(
            [
                lang.add_ticker(),
            ]
        )
        buttons.append(
            [
                lang.back(),
            ]
        )
        markup = self.generate_reply_markup(buttons=buttons)
        return markup

    def back_kb(self):
        buttons =[
                [
                    lang.back(),
                ]
            ]

        markup = self.generate_reply_markup(buttons=buttons)
        return markup

    def redactor_ticker(self, id):
        buttons = [
            [
                {
                    'name': lang.remove_ticker(),
                    'callback': f'ticker_remove_{id}'
                }
            ]
        ]
        markup = self.generate_inline_markup(buttons=buttons)
        return markup

    def redactor_wallet(self):
        buttons = [
            [
                {
                    'name': lang.change_wallet(),
                    'callback': f'wallet_change'
                }
            ]
        ]
        markup = self.generate_inline_markup(buttons=buttons)
        return markup

    def redactor_token(self, id):
        buttons = [
            [
                {
                    'name': lang.remove_token(),
                    'callback': f'token_remove_{id}'
                },
                {
                    'name': lang.set_price(),
                    'callback': f'token_price_{id}'
                }
            ]
        ]
        markup = self.generate_inline_markup(buttons=buttons)
        return markup

    def messages_kb(self, id):
        user = dbase.take_user(id=id)
        messages = user.get('messages')
        if messages:
            name = f'✅ {lang.on()}'
        else:
            name = f'❌ {lang.off()}'
        buttons = [
            [
                {
                    'name': name,
                    'callback': f'message_change'
                },
            ]
        ]
        markup = self.generate_inline_markup(buttons=buttons)
        return markup
kb = keyboards_()