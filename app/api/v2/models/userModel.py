import psycopg2
from flask import jsonify

from .databaseModel import Db

class UserModel(Db):
    """initialize an user object"""
    def __init__(self, name=None, email=None, password=None, role=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

        db = Db()
        db.create_tables()
        self.conn = db.create_connection()

    def saveAdmin(self):
        cursor = self.conn.cursor()
        cursor.execute(
        "INSERT INTO users(name, email, password, role) VALUES(%s, %s, %s, %s)"
        ,(self.name, self.email, self.password, self.role,)
        )
        cursor.execute("SELECT id FROM users WHERE role = %s", (self.role,))
        row = cursor.fetchone()
        self.id  = row[0]
        print(self.id)
        self.conn.commit()
        self.conn.close()

    def get(self):
        db = Db()
        self.conn = db.create_connection()
        db.create_tables()
        cursor = self.conn.cursor()
        mysql = "SELECT * FROM users"
        cursor.execute(mysql)
        users = cursor.fetchall()
        dbusers = []
        for user in users:
            list_of_keys = list(user)
            singleuser = {}
            singleuser["id"] = list_of_keys[0]
            singleuser["name"] = list_of_keys[1]
            singleuser["email"] = list_of_keys[2]
            singleuser["password"] = list_of_keys[3]
            singleuser["role"] = list_of_keys[4]
            dbusers.append(singleuser)
        cursor.close()
        self.conn.close()
        return dbusers
