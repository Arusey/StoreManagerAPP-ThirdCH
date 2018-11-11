from flask import jsonify, make_response, abort
from validate_email import validate_email
import re

from .models.userModel import UserModel
from .models.productsModel import ModelProduct

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
    def validate_details(self, data):
        valid_mail = validate_email(data["email"])
        user = UserModel()
        users = user.getusers()
        for user in users:
            if data["email"] == user["email"]:
                Response = "User already exists"
                abort(406, Response)

        if not valid_mail:
            Response = "The email is not valid"
            abort(400, Response)
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



class ProductValidate(object):
    def __init__(self, data):
        self.data = data


    def validate_empty_products(self):
        if self.data["name"] == "" or self.data["category"] == "" or self.data["description"] == "" or self.data["currentstock"] == "" or self.data["minimumstock"] == "" or self.data["price"] == "":
            Response = "You have to insert a product stored"
            abort(400, Response)
    # def validate_missing_key(self):
    #     '''Checks for missing data keys in data passed during product registration'''
    #     if "name" not in self.data or "category" not in self.data or "description" not in self.data or "currentstock" not in self.data or "minimumstock" not in self.data or "price" not in self.data:
    #         Response = "Must enter all product details"
    #         abort(400, Response)
    def validate_products_data(self):
        myproduct = ModelProduct(self.data)
        products = myproduct.get()
        for product in products:
            if self.data["name"] == product["name"]:
                Response = "Product already registered"
                abort(406, Response)





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
