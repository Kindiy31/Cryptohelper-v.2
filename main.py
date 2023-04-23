from data import bot
import texts
from database import dbase
from keyboards import kb
import markets as mark
import schedule
import time
from threading import Thread
import etherscan
import coinmarketcap
lang = texts.ua

###############################################################################################################################################################


###############################################################################################################################################################

def back_fnc(id):
    bot.send_message(id, lang.start_msg(), reply_markup=kb.home_kb())

###############################################################################################################################################################


#handlers
###############################################################################################################################################################


@bot.message_handler(commands=['start'])
def start(message):
    id = message.from_user.id
    user = dbase.take_user(id=id)
    if not user:
        dbase.register(message)
    bot.send_message(id, lang.start_msg(), reply_markup=kb.home_kb())

@bot.message_handler(content_types=['text'])
def text_handler(message):
    id = message.from_user.id
    user = dbase.take_user(id=id)
    text = message.text

    if text == lang.markets():
        bot.send_message(id, lang.markets_msg(), reply_markup=kb.markets_kb())
    elif text == lang.tokens():
        def reg():
            msg = bot.send_message(id, lang.tokens_msg(), reply_markup=kb.tokens_kb())
            bot.register_next_step_handler(msg, reg_2)
        def reg_2(message):
            text = message.text
            if text == lang.back():
                back_fnc(id=id)
            elif text == lang.add_token():
                msg = bot.send_message(id, lang.insert_pair(), reply_markup=kb.back_kb())
                bot.register_next_step_handler(msg, add_pair)
            else:
                pair = text.split('/')
                if len(pair) != 2:
                    msg = bot.send_message(id, lang.error_format(), reply_markup=kb.back_kb())
                    bot.register_next_step_handler(msg, reg_2)
                    return
                ticker_1 = pair[0]
                ticker_2 = pair[1]
                token = dbase.take_token(name=text)
                id_token = token.get('ID')
                msg_text = mark.take_price_for_pair(ticker_1=ticker_1, ticker_2=ticker_2)
                msg = bot.send_message(id, msg_text, reply_markup=kb.redactor_token(id=id_token))
                bot.register_next_step_handler(msg, reg_2)
        def add_pair(message):
            text = message.text
            if text == lang.back():
                back_fnc(id=id)
            else:
                dbase.add_token(name=text)
                bot.send_message(id, lang.pair_append(name=text), reply_markup=kb.home_kb())
        reg()

    elif text == lang.tickers():
        def reg():
            msg = bot.send_message(id, lang.tickers_msg(), reply_markup=kb.tickers_kb())
            bot.register_next_step_handler(msg, reg_2)
        def reg_2(message):
            text = message.text
            if text == lang.back():
                back_fnc(id=id)
            elif text == lang.add_ticker():
                msg = bot.send_message(id, lang.insert_ticker(), reply_markup=kb.back_kb())
                bot.register_next_step_handler(msg, add_ticker)
            else:
                info = coinmarketcap.get_info(ticker=text)
                if not info:
                    msg = bot.send_message(id, lang.ticker_denided(), reply_markup=kb.tickers_kb())
                    bot.register_next_step_handler(msg, reg_2)
                    return
                ticker = dbase.take_ticker(name=text)
                id_ticker = ticker.get('ID')
                msg = bot.send_message(id, lang.ticker_info(info), reply_markup=kb.redactor_ticker(id=id_ticker), parse_mode='Markdown')
                bot.register_next_step_handler(msg, reg_2)
        def add_ticker(message):
            text = message.text
            if text == lang.back():
                back_fnc(id=id)
            else:
                dbase.add_ticker(name=text)
                bot.send_message(id, lang.ticker_append(name=text), reply_markup=kb.home_kb())
        reg()

    elif text == lang.wallet():
        address = user.get('address')
        if address:
            balance = etherscan.get_balance_for_address(address=address)
            tickers = ['USDT', 'BTC', 'UAH']
            equivalents = []
            for ticker in tickers:

                price = mark.take_price_for_pair('ETH', ticker, one_price=True)
                if price:
                    price = price.get('ETH')
                equivalents.append(
                    {
                        ticker:
                            {
                                'price': price,
                                'equivalent': round(float(eval(f'{balance} * {price}')), 6)
                            }
                    }
                )
            if not balance:
                balance = 'Помилка, можливо ви ввели не вірний гаманець?'


            bot.send_message(id, lang.your_wallet(address=address,
                                                  equivalents=equivalents, balance=balance), parse_mode='Markdown',
                             reply_markup=kb.redactor_wallet())
        else:
            def reg():
                msg = bot.send_message(id, lang.no_wallet(), reply_markup=kb.back_kb())
                bot.register_next_step_handler(msg, reg_2)
            def reg_2(message):
                text = message.text
                if text == lang.back():
                    back_fnc(id=id)
                else:
                    dbase.update_address(id=id, address=text)
                    bot.send_message(id, lang.new_address(address=text), reply_markup=kb.home_kb())
            reg()

    elif text == lang.messages():
        bot.send_message(id, lang.messages_msg(), reply_markup=kb.messages_kb(id=id))

    else:
        back_fnc(id=id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    id = call.from_user.id
    callb = call.data
    state = callb.split("_")
    if state[0] == 'market':
        if state[1] == 'change':
            id_market = state[2]
            dbase.change_market(id=id_market)
            bot.edit_message_text(chat_id=id, message_id=call.message.id,
                                  text=call.message.text, reply_markup=kb.markets_kb())

    elif state[0] == 'ticker':
        if state[1] == 'remove':
            id_ticker = state[2]
            dbase.delete_ticker(id=id_ticker)
            bot.edit_message_text(chat_id=id, message_id=call.message.id,
                                  text=call.message.text)
            bot.send_message(id, lang.ticker_remove_approved(), reply_markup=kb.tickers_kb())

    elif state[0] == 'token':
        if state[1] == 'remove':
            id_token = state[2]
            dbase.delete_token(id=id_token)
            bot.edit_message_text(chat_id=id, message_id=call.message.id,
                                  text=call.message.text)
            bot.send_message(id, lang.token_remove_approved(), reply_markup=kb.tokens_kb())
        elif state[1] == 'price':
            bot.clear_step_handler_by_chat_id(id)
            id_token = state[2]
            def reg():
                token = dbase.take_token(id=id_token)
                if token:
                    name = token.get('name')
                    ticker_1 = name.split('/')[0]
                    ticker_2 = name.split('/')[-1]
                    price_now = mark.take_price_for_pair(ticker_1=ticker_1,
                                                         ticker_2=ticker_2,
                                                         one_price=True)
                    msg = bot.send_message(id, lang.how_price(price_now=price_now), reply_markup=kb.back_kb())
                    bot.register_next_step_handler(msg, reg_2, name)
                else:
                    bot.send_message(id, lang.error())

            def reg_2(message, name):
                text = message.text
                if text == lang.back():
                    back_fnc(id)
                    return
                try:
                    price = float(text)
                    result = dbase.set_price(id=id_token, price=price, id_user=id)
                    if result:
                        bot.send_message(id, lang.we_send_you(name=name, price=price), reply_markup=kb.back_kb())
                    else:
                        bot.send_message(id, lang.error())
                except:
                    bot.send_message(id, lang.error())
            reg()

    elif state[0] == 'message':
        if state[1] == 'change':
            dbase.change_messages(id=id)
            bot.edit_message_text(chat_id=id, message_id=call.message.id,
                                  text=call.message.text, reply_markup=kb.messages_kb(id=id))

    elif state[0] == 'wallet':
        if state[1] == 'change':
            def reg():
                msg = bot.send_message(id, lang.insert_new_wallet(), reply_markup=kb.back_kb())
                bot.register_next_step_handler(msg, reg_2)
            def reg_2(message):
                text = message.text
                if text == lang.back():
                    back_fnc(id=id)
                    return
                dbase.update_address(id=id, address=text)
                bot.send_message(id, lang.wallet_updated(), reply_markup=kb.home_kb())
            reg()
###############################################################################################################################################################


#schedule function
###############################################################################################################################################################

def check_prices():
    print('Run check prices!')
    active_transactions = dbase.take_transactions()
    for transaction in active_transactions:
        token_id = transaction.get('token_id')
        token = dbase.take_token(id=token_id)
        if token:
            is_low = transaction.get('is_low')
            id_transction = transaction.get('id')
            need_price = transaction.get('need_price')
            name = token.get('name')
            ticker_1 = name.split('/')[0]
            ticker_2 = name.split('/')[-1]
            price_now = mark.take_price_for_pair(ticker_1=ticker_1,
                                                 ticker_2=ticker_2,
                                                 one_price=True)
            if price_now:
                price_now = next(iter(price_now.values()))
                result = False
                if is_low:
                    if float(price_now) < float(need_price):
                        result = True
                else:
                    if float(price_now) > float(need_price):
                        result = True
                if result:
                    dbase.finish_transaction(id=id_transction)
                    id_user = transaction.get('id_user')
                    bot.send_message(id_user, lang.price_changed(name=name, price=need_price))
def check_transactions():
    print('Check users transaction...')
    users = dbase.take_users()

    #Фільтруємо і залишаємо лише тих, у кого є гаманець та увімкнені повідомлення за допомогою lambda
    users = list(filter(lambda x: x.get('address') and x.get('messages'), users))

    for user in users:
        last_hash = user.get('last_hash')
        address = user.get('address')
        id_user = user.get('ID')
        check_hash = etherscan.take_last_transaction(address=address)
        if check_hash:
            if last_hash:
                if last_hash != check_hash.get('hash'):
                    bot.send_message(id_user, lang.new_transaction(check_hash=check_hash, address=address), parse_mode='Markdown')
                    dbase.update_hash(id=id_user, hash=check_hash.get('hash'))

            else:
                dbase.update_hash(id=id_user, hash=check_hash.get('hash'))



###############################################################################################################################################################


#Run project
###############################################################################################################################################################

def do_schedule():
    schedule.every(30).seconds.do(check_prices)
    schedule.every(30).seconds.do(check_transactions)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as a:
            print(a)

if __name__ == '__main__':
    scheduler = Thread(target=do_schedule)
    scheduler.start()
    print("Bot starting...")
    bot.polling(True)

###############################################################################################################################################################

