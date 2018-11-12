import psycopg2
from flask import make_response, jsonify

from .databaseModel import Db

class ModelSales(Db):
    '''initialize a sale'''

    def __init__(self, userid=None, productid=None):
        self.userid = userid
        self.productid = productid

        self.db = Db()
        self.conn = self.db.create_connection()

    def save(self, userid, id):
        '''record a sale'''
        print(userid, "\n\n\n\n\n\n")
        self.db.create_tables()
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO sales(userid, productid) VALUES(%s, %s)",
                (self.userid, self.productid),)
        except Exception as e:
            print(e)

        self.conn.commit()
        self.conn.close()

    def get_all_sales(self):
        db = Db()
        self.conn = db.create_connection()
        db.create_tables()
        cursor = self.conn.cursor()

        cursor.execute("SELECT products.id, products.name, products.category, products.description, products.price, sales.id, users.id, users.name, products.currentstock FROM products JOIN sales ON products.id=sales.productid JOIN users ON users.id=sales.userid")
        result = cursor.fetchall()
        sales = []
        for single_item in result:
            sale = {}
            sale['productid'] = single_item[0]
            sale['productname'] = single_item[1]
            sale['category'] = single_item[2]
            sale['description'] = single_item[3]
            sale['price'] = single_item[4]
            sale['saleid'] = single_item[5]
            sale['attendantid'] = single_item[6]
            sale['attendantname'] = single_item[7]
            sale['quantity'] = single_item[8]
            sales.append(sale)


        return sales
