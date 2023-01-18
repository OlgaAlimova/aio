import sqlite3

class DataBase:
    def __init__(self, db_path: str = 'data_base/bot_db.db'):
        self.db_path = db_path

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_goods(self):
        sql = '''CREATE TABLE IF NOT EXISTS goods
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        g_type TEXT, image TEXT, name TEXT,
        desc TEXT, quantity INTEGER, price REAL)'''
        self.execute(sql, commit=True)

    def create_table_basket(self):
        sql = '''CREATE TABLE IF NOT EXISTS basket
        (id_order INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER, id_goods INTEGER)'''
        self.execute(sql, commit=True)

    def create_table_purchase(self):
        sql = '''CREATE TABLE IF NOT EXISTS purchase
        (id_order INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone_number TEXT, email TEXT,
        shipping TEXT, address TEXT, goods TEXT)'''
        self.execute(sql, commit=True)

    def add_goods(self, goods: dict):
        parameters = (goods.get('g_type'), goods.get('image'), goods.get('name'),
                      goods.get('desc'), goods.get('quantity'), goods.get('price'))
        sql = '''INSERT INTO goods(g_type, image, name, desc, quantity, price)
        VALUES (?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def get_goods(self, **kwargs):
        sql = '''SELECT * FROM goods WHERE'''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_basket(self, **kwargs):
        sql = '''SELECT * FROM basket WHERE'''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def add_to_basket(self, id_user: int, id_goods: int):
        parameters = (id_user, id_goods)
        sql = '''INSERT INFO basket (id_user, id_good) VALUES (?, ?)'''
        self.execute(sql, parameters, commit=True)
        parameters = (id_goods,)
        sql = '''UPDATE goods SET quantity - 1 WHERE id=?'''
        self.execute(sql, parameters, commit=True)

    def remove_from_basket(self, id_order: int, id_goods: int):
        parameters = (id_order,)
        sql = '''DELETE FROM basket WHERE id_order=?'''
        self.execute(sql, parameters, commit=True)
        parameters = (id_goods,)
        sql = '''UPDATE goods SET quantity = quantity + 1 WHERE id=?'''
        self.execute(sql, parameters, commit=True)

    def clear_basket(self, id_user):
        parameters = (id_user,)
        sql = '''DELETE FROM basket WHERE id_user=?'''
        self.execute(sql, parameters, commit=True)

    def add_purchase(self, id_user: int, order: dict, shipping:str):
        sql = '''INSERT INTO purchase (name, phone_number, email, shipping, address, goods)
        VALUES (?, ?, ?, ?, ?, ?)'''
        for goods in self.get_basket(id_user=id_user):
            item = self.get_goods(id=int(goods[2]))
            parameters = (order.get('name'), order.get('phone_number'), order.get('email'),
                          shipping, str(order.get('shipping_address')), str(item[0][3]))
            self.execute(sql, parameters, commit=True)

    @staticmethod
    def extract_kwargs(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())

    def disconnect(self):
        self.connection.close()
