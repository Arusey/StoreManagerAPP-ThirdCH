from flask import jsonify, make_response, abort
from validate_email import validate_email
import re

from .models.userModel import UserModel
from .models.productModel import ModelProduct


class AuthValidate(object):
    def __init__(self, data):
        self.data = data
    """docstring for AuthValidate."""


    def validate_invalid_entry(self, data):


        if " " in data["name"]:
            Response = "Remove space in name"
            abort(400, Response)
        if " " in data["email"]:
            Response = "Remove space in email"
            abort(400, Response)
        if " " in data["password"]:
            Response = "Remove space in password"
            abort(400, Response)
        if " " in data["role"]:
            Response = "Remove space in role"
            abort(400, Response)
    def validate_empty_data(self, data):
        if data["name"] =="" or data["email"] =="" or data["password"] =="" or data["role"] =="":
            Response ="Missing credentials, check again"
            abort(400, Response)
    # def validate_data(self, data):
    #     if type(data["name"]) is not str or type(data["email"]) is not str or type(data["password"]) is not str or type(data["role"]) is not str:
    #         Response = "You cannot insert an integer"
    #         abort(400, Response)
    def validate_details(self, data):
        valid_mail = validate_email(data["email"])
        users = UserModel.get(self)
        for user in users:
            if data["email"] == user["email"]:
                Response = "User already exists"
                abort(406, Response)

        if not valid_mail:
            Response = "The email is not valid"
            abort(400, Response)
        # if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", self.data["email"]):
        #     Response = "Email must have a fullstop"
        #     abort(400, Response)
        elif len(data["password"]) < 6 or len(data["password"]) > 12:
            Response = "Password must be long than 6 characters or less than 12"
            abort(400, Response)
        elif not any(char.isdigit() for char in data["password"]):
            Response = "Password must have a digit"
            abort(400, Response)
        elif not any(char.isupper() for char in data["password"]):
            Response = "Password must have an upper case character"
            abort(400, Response)
        elif not any(char.islower() for char in data["password"]):
            Response = "Password must have a lower case character"
            abort(400, Response)
        elif not re.search("^.*(?=.*[@#$%^&+=]).*$", data["password"]):
            Response = "Password must have a special charater"
            abort(400, Response)



    def validate_datatypes(self, data):
        if type(self.data["name"]) is not str:
            Response = "Only string characters allowed for name"
            abort(400, Response)
        if type(self.data["email"]) is not str:
            Response = "Only string characters are allowed for email"
            abort(400, Response)
        if type(self.data["password"]) is not str:
            Response = "Only string characters are allowed for password"
            abort(400, Response)
        if type(self.data["role"]) is not str:
            Response = "Only string characters are allowed for role"
            abort(400, Response)

    def validate_missing_key(self, data):
        '''Checks for missing data keys in data passed during product registration'''
        if "name" not in data or "category" not in data or "description" not in data or "currentstock" not in data or "minimumstock" not in data or "price" not in data:
            Response = "Must enter all product details"
            abort(400, Response)







class ProductValidate(object):
    def __init__(self, data):
        self.data = data


    def validate_empty_products(self, data):
        print(data)
        if data["name"] == "" or data["category"] == "" or data["description"] == "" or data["currentstock"] == "" or data["minimumstock"] == "" or data["price"] == "":
            Response = "You have to insert a product stored"
            abort(400, Response)
    def validate_missing_key(self, data):
        '''Checks for missing data keys in data passed during product registration'''
        if "name" not in data or "category" not in data or "description" not in data or "currentstock" not in data or "minimumstock" not in data or "price" not in data:
            Response = "Must enter all product details"
            abort(400, Response)
    def validate_products_data(self, data):
        myproduct = ModelProduct(data)
        products = myproduct.get()
        for product in products:
            if data["name"] == product["name"]:
                Response = "Product already registered"
                abort(406, Response)
        if " " in data["name"] or " " in data["category"]:
            Response = "Ensure no spaces when entering detail"
            abort(400, Response)




class SalesValidate(object):
    def __init__(self, data):
        self.data = data

    def validate_sales_datatype(self):
        if type(self.data["id"]) is not int:
            Response = "Ensure you have filled up the correct number of fields"
            abort(400, Response)


    def validate_empty_sales_data(self):
        '''checks whether data is empty when making a sale'''
        if not self.data:
            Response = "Ensure details have been inserted"
            abort(400, Response)

        if "id" not in self.data:
            Response = "Product id key is missing"
            abort(400, Response)
