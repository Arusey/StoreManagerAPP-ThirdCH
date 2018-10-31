from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import Config
import jwt
import datetime

from .models.userModel import UserModel
from .models.productModel import ModelProduct
from .models.salesModel import ModelSales
from .utils import AuthValidate, ProductValidate

def token_required(func):
    '''creates a token'''
    @wraps(func)
    def decorated(*args, **kwargs):

        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({
                                 "Message": "the access token is missing, Login"}, 401))
        try:
            data = jwt.decode(
               token, Config.SECRET_KEY, algorithms=['HS256'])
            print(data)
            newuser = UserModel()
            users = newuser.get()
            for user in users:

                if user['email'] == data['email']:
                    current_user = user
        except Exception as e:
            print(e)
            return make_response(jsonify({
                "Message": "This token is invalid"
            }), 403)

        return func(current_user, *args, **kwargs)
    return decorated



class AdminSignup(Resource):
    """docstring for AdminSignup."""
    def post(self):
        data = request.get_json()
        AuthValidate.validate_missing_key_value(self, data)
        AuthValidate.validate_data(self, data)
        AuthValidate.validate_invalid_entry(self,data)
        AuthValidate.validate_empty_data(self, data)
        AuthValidate.validate_details(self, data)
        name = data["name"]
        email = data["email"]
        password = data["password"]
        role = data["role"]
        user = UserModel(name, email, password, role)
        user.saveAdmin()
        message = make_response(jsonify({
        "Message": "user successfully registered",
        "name": name,
        "email": email,
        "role": role
        }), 201)
        return message
class AttSignup(Resource):
    """docstring for attendant Signup."""
    @token_required
    def post(current_user, self):
        data = request.get_json()
        if current_user and current_user["role"] == "admin":
            AuthValidate.validate_missing_key_value(self, data)
            AuthValidate.validate_data(self, data)
            AuthValidate.validate_invalid_entry(self,data)
            AuthValidate.validate_empty_data(self, data)
            AuthValidate.validate_details(self, data)
            name = data["name"]
            email = data["email"]
            password = data["password"]
            role = data["role"]
            attendant = UserModel(name, email, password, role)
            attendant.saveAdmin()
            message = make_response(jsonify({
            "Message": "user successfully registered",
            "name": name,
            "email": email,
            "role": role
            }), 201)
            return message
        message = make_response(jsonify({
            "message": "please login as administrator"
        }), 401)
        return message
