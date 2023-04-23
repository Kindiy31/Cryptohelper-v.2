import sqlite3
import texts
class db:
    def __init__(self):
        self.con = sqlite3.connect('database.db', timeout=10, check_same_thread=False)
        self.cur = self.con.cursor()
        self.con.commit()
    def select_sqlite(self, table, values='*', where='', fetchall=False, cursor_dict=False):
        result = []
        if where != '':
            where = f"WHERE {where}"
        sql = f"SELECT {values} FROM {table} {where};"
        #print(sql)
        self.cur.execute(sql)
        columns = [column[0] for column in self.cur.description]
        if fetchall:
            rows = self.cur.fetchall()
            if cursor_dict:
                for row in rows:
                    result.append(dict(zip(columns, row)))
            else:
                result = rows
        else:
            result = self.cur.fetchone()
            if result:
                if cursor_dict:
                    result = dict(zip(columns, result))
        return result

    def update_sqlite(self, table, column, value, where=''):
        if where != '':
            where = f'WHERE {where}'
        self.cur.execute(f'UPDATE {table} SET {column} = "{value}" {where}')
        self.con.commit()
        return True

    def insert_sqlite(self, table, columns_list, data):
        columns = ''
        VALUES = ''
        for value in columns_list:
            columns += f'{value}, '
            VALUES += '?,'
        columns = columns[:-2]
        VALUES = VALUES[:-1]
        sql = f'INSERT INTO {table} ({columns}) VALUES({VALUES})'
        self.cur.execute(sql, data)
        self.con.commit()
        return True

    def delete_sqlite(self, table, where=''):
        if where != '':
            where = f'WHERE {where}'
        sql = f'DELETE FROM {table} {where}'
        self.cur.execute(sql)
        self.con.commit()

    def take_markets(self):
        markets = self.select_sqlite(table=texts.dbase_markets, fetchall=True, cursor_dict=True)
        return markets

    def take_market(self, id):
        market = self.select_sqlite(table=texts.dbase_markets, cursor_dict=True, where=f'ID = {id}')
        return market

    def change_messages(self, id):
        user = self.take_user(id=id)
        if user:
            if not user.get('messages'):
                self.update_sqlite(table=texts.dbase_users, column='messages', value=1, where=f"ID = {id}")
            elif user.get('messages'):
                self.update_sqlite(table=texts.dbase_users, column='messages', value=0, where=f"ID = {id}")

    def change_market(self, id):
        market = self.take_market(id=id)
        if market:
            if not market.get(texts.is_active):
                self.update_sqlite(table=texts.dbase_markets, column=texts.is_active, value=1, where=f"ID = {id}")
            elif market.get(texts.is_active):
                self.update_sqlite(table=texts.dbase_markets, column=texts.is_active, value=0, where=f"ID = {id}")
        markets = self.take_markets()
        return markets

    def take_user(self, id):
        user = self.select_sqlite(table=texts.dbase_users, where=f'ID = {id}', cursor_dict=True)
        return user

    def take_users(self):
        users = self.select_sqlite(table=texts.dbase_users, fetchall=True, cursor_dict=True)
        return users

    def register(self, message):
        info_user = message.from_user
        id = info_user.id
        first_name = info_user.first_name
        username = info_user.username
        column = ['id', 'first_name', 'username', 'address', 'messages']
        values = [id, first_name, username, None, False]
        self.insert_sqlite(table=texts.dbase_users, columns_list=column, data=values)
        return True

    def add_ticker(self, name):
        self.insert_sqlite(table='tickers', columns_list=('name',), data=[name, ])

    def delete_ticker(self, id):
        self.delete_sqlite(table='tickers', where=f'ID = {id}')

    def take_tickers(self):
        tokens = self.select_sqlite(table='tickers', fetchall=True, cursor_dict=True)
        return tokens

    def take_ticker(self, id='', name=''):
        token = None
        if id:
            token = self.select_sqlite(table='tickers', where=f'ID={id}', cursor_dict=True)
        elif name:
            token = self.select_sqlite(table='tickers', where=f"name='{name}'", cursor_dict=True)
        return token

    def add_token(self, name):
        self.insert_sqlite(table=texts.dbase_tokens, columns_list=('name', ), data=[name, ])

    def delete_token(self, id):
        self.delete_sqlite(table=texts.dbase_tokens, where=f'ID = {id}')

    def take_tokens(self):
        tokens = self.select_sqlite(table='tokens', fetchall=True, cursor_dict=True)
        return tokens

    def take_token(self, id='', name=''):
        token = None
        if id:
            token = self.select_sqlite(table=texts.dbase_tokens, where=f'ID={id}', cursor_dict=True)
        elif name:
            token = self.select_sqlite(table=texts.dbase_tokens, where=f"name='{name}'", cursor_dict=True)
        return token

    def create_transaction(self, id_user, token_id, start_price, need_price, is_finish=False):
        try:
            columns = ('id_user', 'token_id', 'start_price', 'need_price', 'is_low', 'is_finish')
            if float(start_price) > float(need_price):
                is_low = True
            else:
                is_low = False
            values = [id_user, token_id, start_price, need_price, is_low, is_finish]
            self.insert_sqlite(table='transactions', columns_list=columns, data=values)
            return True
        except Exception as a:
            print(a)

    def set_price(self, id, price, id_user):
        import markets as mark
        token = self.take_token(id=id)
        if token:
            name = token.get('name')
            ticker_1 = name.split('/')[0]
            ticker_2 = name.split('/')[-1]
            price_now = mark.take_price_for_pair(ticker_1=ticker_1,
                                                 ticker_2=ticker_2,
                                                 one_price=True)
            if price_now:
                result = self.create_transaction(id_user=id_user, token_id=id,
                                        start_price=next(iter(price_now.values())), need_price=price)
                if result:
                    return True

    def take_transactions(self, is_finish=False, all=False):
        if all:
            transactions = self.select_sqlite(table='transactions', fetchall=True, cursor_dict=True)
        else:
            if not is_finish:
                transactions = self.select_sqlite(table='transactions', where='is_finish = 0', fetchall=True, cursor_dict=True)
            else:
                transactions = self.select_sqlite(table='transactions', where='is_finish = 1', fetchall=True, cursor_dict=True)
        return transactions

    def finish_transaction(self, id):
        self.update_sqlite(table='transactions', column='is_finish', value=1, where=f'id={id}')

    def update_address(self, id, address):
        self.update_sqlite(table='users', column='address', value=address, where=f'ID={id}')

    def update_hash(self, id, hash):
        self.update_sqlite(table='users', column='last_hash', value=hash, where=f'ID={id}')

dbase = db()
