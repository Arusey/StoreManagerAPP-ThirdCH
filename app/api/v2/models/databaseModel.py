import psycopg2
from flask import jsonify
import os
from instance.config import Config

from sys import modules


class Db(object):
    def __init__(self):
        self.conn = None


    def create_connection(self):
        '''trying to create a connection to the database'''
        try:
            if 'pytest' in modules:
                URL = "test_database"
            elif os.getenv("APP_SETTINGS") == "development":
                URL = "storemanager"
            self.conn = psycopg2.connect(database=URL)

        except Exception as e:
            print(e)
            self.conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode = 'require')
        self.conn.autocommit = True
        return self.conn


    def close_connection(self):
        '''this is a method that closes the database connections'''
        return self.conn.close()

    def create_tables(self):
        cursor = self.create_connection().cursor()
        tables = [
            """CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            name varchar(80) NOT NULL,
            email varchar(80) NOT NULL UNIQUE,
            password varchar(80) NOT NULL,
            role varchar(10) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS products(
            id serial PRIMARY KEY UNIQUE,
            name varchar(15) NOT NULL,
            category varchar(20) NOT NULL,
            description varchar(80) NOT NULL,
            currentstock int NOT NULL,
            minimumstock int NOT NULL,
            price float(40) NOT NULL
            )""",

            """CREATE TABLE IF NOT EXISTS sales(
            id serial PRIMARY KEY ,
            userId int REFERENCES users(id) not null,
            productid int REFERENCES products(id) ON DELETE CASCADE ON UPDATE CASCADE


            )""",
            """CREATE TABLE IF NOT EXISTS badtokens(
                id serial PRIMARY KEY,
                token varchar(255) NOT NULL,
                date varchar(255) NOT NULL
            )"""
               ]

        try:
            for table in tables:
                cursor.execute(table)
            cursor.execute(
                """INSERT INTO users(name, email, password, role)
                VALUES('tony','tony@email.com','kevin@123','admin');"""
            )
        except Exception as e:
            print(e)
            return "error"

        self.conn.commit()
        self.conn.close()

    def collapse_tables(self):
        cursor = self.create_connection().cursor()
        cursor.execute(
             "SELECT table_schema,table_name FROM information_schema.tables "
            " WHERE table_schema = 'public' ORDER BY table_schema,table_name"
        )
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("drop table "+row[1] + " cascade")
        self.conn.commit()
        self.conn.close()
