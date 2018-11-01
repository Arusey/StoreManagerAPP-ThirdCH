from flask import jsonify, make_response, abort
from validate_email import validate_email
import re

from .models import users, products


class AuthValidate(object):
    """docstring for AuthValidate."""
    def validate_empty_data(self, data):
        if data["name"] =="" or data["email"] =="" or data["password"] =="" or data["role"] =="":
            Response ="Response please insert your credentials"
            abort(400, Response)
    def validate_data(self, data):
        if type(data["name"]) is not str or type(data["email"]) is not str or type(data["password"]) is not str or type(data["role"]) is not str:
            Response = "You cannot insert an integer"
            abort(400, Response)
    def validate_details(self, data):
        valid_mail = validate_email(data["email"])
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
        if " " in data["email"]:
            Response = "Remove space in email"
            abort(400, Response)
        if " " in data["name"]:
            Response = "Remove space in name"
            abort(400, Response)
        if " " in data["password"]:
            Response = "Remove space in password"
            abort(400, Response)
        if " " in data["role"]:
            Response = "Remove space in role"
            abort(400, Response)


class ProductValidate(object):
    def validate_empty_products(self, data):
        if data["name"] == "" or data["category"] == "" or data["description"] == "" or data["currentstock"] == "" or data["minimumstock"] == "" or data["price"] == "":
            Response = "You have to insert a product stored"
            abort(400, Response)
        for product in products:
            if data["name"] == product["name"]:
                Response = "Product already registered"
                abort(404, Response)
        if " " in data["name"]:
            Response = "Remove space in name"
            abort(400, Response)
        if " " in data["category"]:
            Response = "Remove space in category"
            abort(400, Response)
