import sqlite3,math
from .models import Product, User

class Database:
    def __init__(self, db_name = "db.sqlite3"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.c.execute(query)
        self.conn.commit()

    def select_one(self, table_name, id,condition = ""):
        query = f"SELECT * FROM {table_name} WHERE id = ? {condition}"
        self.c.execute(query, (id,))
        item =  self.c.fetchone()
        return {'id': item[0], 'title': item[1], 'description': item[2], 'body': item[3], 'image': item[4]}
    
    def select_latest(self,table_name,condition=""):
        query = f"SELECT * FROM {table_name} "
        if condition:
            query += f"WHERE {condition}"
        query += "ORDER BY id DESC"
        self.c.execute(query)
        item =  self.c.fetchone()
        return {'id': item[0], 'title': item[1], 'description': item[2], 'body': item[3] ,'image': item[4]}

    def update(self, table_name, id, values):
        query = f"UPDATE {table_name} SET {', '.join([f'{column} = ?' for column in values.keys()])} WHERE id = ?"
        self.c.execute(query, (*values.values(), id))
        self.conn.commit()

    def delete(self, table_name, id):
        query = f"DELETE FROM {table_name} WHERE id = ?"
        self.c.execute(query, (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

class ProductDatabase(Database):

    def create_table(self):
        columns = []
        query = f"CREATE TABLE IF NOT EXISTS 'shop_app_product' ({', '.join(columns)})"
        self.c.execute(query)
        self.conn.commit()

    def select_all_by_ids(self, uhf_ids= []):
        uhf_ids = [f"`{i}`" for i in uhf_ids]
        query = f"SELECT `id`,`name`,`price`,`image`,`uhf_id` FROM 'shop_app_product' WHERE uhf_id in ({','.join(uhf_ids)})"
        self.c.execute(query)
        items = self.c.fetchall()
        result = []
        for item in items:
            if not item[4]:
                item[4] = ''
            result.append(Product(id=str(item[0]),name=item[1],price=item[2],image_url=item[3], uhf_id=str(item[4])))
        return result

class UserDatabase(Database):
    def create_table(self):
        columns = []
        query = f"CREATE TABLE IF NOT EXISTS 'shop_app_customuser' ({', '.join(columns)})"
        self.c.execute(query)
        self.conn.commit()

    def select_data_by_id(self, id = None):
        query = f"SELECT `id`,`username` FROM 'shop_app_customuser' WHERE id = ?"
        self.c.execute(query,(id,))
        item = self.c.fetchone()
        return User(id=item[0], name=item[1])