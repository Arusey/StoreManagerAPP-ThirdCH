import psycopg2
from flask import make_response, jsonify



from .databaseModel import Db


class ModelProduct(Db):
    '''initialize a new product'''

    def __init__(self, data=None):
        self.data = data
        db = Db()
        db.create_tables()
        self.conn = db.create_connection()

    def add_product(self):
        '''add product by appending it to the product tables'''
        print(self.data)
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO products(name, category, description, currentstock, minimumstock, price) VALUES(%s, %s, %s, %s, %s, %s)", (self.data["name"], self.data["category"], self.data["description"], self.data["currentstock"], self.data["minimumstock"], self.data["price"])
            )
        except Exception as e:
            print(e)
        self.conn.commit()
        self.conn.close()
    def get(self):
        db = Db()
        self.conn = db.create_connection()
        db.create_tables()
        cursor = self.conn.cursor()
        mysql = "SELECT * FROM products"
        cursor.execute(mysql)
        products = cursor.fetchall()
        totalproducts = []
        for product in products:
            list_of_keys = list(product)
            singleproduct = {}
            singleproduct["id"] = list_of_keys[0]
            singleproduct["name"] = list_of_keys[1]
            singleproduct["category"] = list_of_keys[2]
            singleproduct["description"] = list_of_keys[3]
            singleproduct["currentstock"] = list_of_keys[4]
            singleproduct["minimumstock"] = list_of_keys[5]
            singleproduct["price"] = list_of_keys[6]
            totalproducts.append(singleproduct)
        self.conn.commit()
        return totalproducts
    def delete(self, id):
        self.id = id
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE from products WHERE id = %s",
            (self.id,)
        )
        self.conn.commit()
        self.conn.close()
    def update(self, id):
        '''update product details by editing it'''
        db = Db()
        self.conn = db.create_connection()
        db.create_tables()
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE products SET name = %s, currentstock = %s, price = %s WHERE id = %s""", (self.data["name"],
             self.data["currentstock"], self.data["price"], id))

        print(self.data)
        self.conn.commit()
        self.conn.close()
