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
class AdminLogin(Resource):
    '''docstring for administrator login'''
    def post(self):
        '''login as user and encode a jwt token'''
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        users = UserModel.get(self)
        for user in users:
            if email == user["email"] and password == user['password']:


                token = jwt.encode({
                "email": email,
                "password" : password,
                "exp": datetime.datetime.utcnow() + datetime.timedelta
                                                (minutes=50000)
                }, Config.SECRET_KEY, algorithm='HS256')
                return make_response(jsonify({
                            "Message": "user successfully logged in",
						     "token": token.decode("UTF-8")}), 200)
            return make_response(jsonify({
                "Message": "Login failed, wrong entries"
            }
            ), 403)
class AttLogin(Resource):
    '''docstring for attendant login'''
    def post(self):
        '''login as attendant and encode a jwt token'''
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        users = UserModel.get(self)
        for user in users:
            if email == user["email"] and password == user["password"]:
                print(user)
                token = jwt.encode({
                "email": email,
                "password" : password,
                "exp": datetime.datetime.utcnow() + datetime.timedelta
                                                (minutes=54567)
                }, Config.SECRET_KEY, algorithm='HS256')
                return make_response(jsonify({
                            "Message": "attendant successfully logged in",
						     "token": token.decode("UTF-8")}), 200)
            return make_response(jsonify({
                            "Message": "Check your credentials",
                                "Status": "Failed"}), 401)



class Product(Resource):
    @token_required
    def post(current_user, self):
        '''endpoint for posting a product'''
        if current_user and current_user["role"] != "admin":
            return make_response(jsonify({
                "Message": "you must be an admin endpoint"}
            ), 403)
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                "Message": "Kindly ensure you have inserted your details"
            }), 400)
        ProductValidate.validate_missing_key(self, data)
        ProductValidate.validate_empty_products(self, data)
        ProductValidate.validate_products_data(self, data)


        name = data["name"]
        category = data["category"]
        description = data["description"]
        currentstock = data["currentstock"]
        minimumstock = data["minimumstock"]
        price = data["price"]

        product = ModelProduct(data)
        product.add_product()
        return make_response(jsonify({
            "Status": "ok",
            "Message": "Product posted successfully",
            "Products": product.get()
        }
        ), 201)

    @token_required
    def get(current_user, self):
        '''endpoint for getting all products'''

        if current_user:
            product = ModelProduct()
            products = product.get()
            if len(products) == 0:
                return  make_response(jsonify({
                    "Message": "No products have been posted yet"
                }), 404)
            return make_response(jsonify({
                "Status": "ok",
                "Message": "All products fetched successfully",
                "products": products
            }
            ), 200)
        return make_response(jsonify({
            "Message": "Please login first"
        }), 401)
        @token_required
    def put(current_user, self, id):
        '''update details in product'''
        if current_user and current_user["role"] != "admin":
            return make_response(jsonify({
                "Message": "You have to be an admin"
            }), 403)
        data = request.get_json()
        name = data["name"]

        currentstock = data["currentstock"]

        price = data["price"]

        product = ModelProduct(data)
        products = product.get()

        if len(products) == 0:
            return make_response(jsonify(
            {
                "Message": "No products have been posted yet"
            }
            ), 404)

        for item in products:
            if int(id) == int(item["id"]):
                product.update(id)
                return make_response(jsonify({
                    "Message": "product has been updated successfully",
                    "product": product.get()
                }), 200)
        return make_response(jsonify({
            "Message": "The product does not exist"
        }), 404)


class SingleProduct(Resource):
    '''docstring for getting a single sale'''
    @token_required
    def get(current_user, self, id):
        '''gets single product'''
        product = ModelProduct()
        products = product.get()
        if len(products) == 0:
            return make_response(jsonify({
                "Message": "No products have been posted yet"
            }), 404)
        if current_user:
            for product in products:
                if int(id) == product["id"]:
                    return make_response(jsonify({
                    "Message": "Product retrieval successful",
                    "product": product
                    }), 200)
        return make_response(jsonify({
            "Message": "This product does not exist"
        }), 404)

class Sale(Resource):
    @token_required
    def post(current_user, self):
        total = 0
        data = request.get_json()
        if not data or not data["id"]:
            return make_response(jsonify({

                "Message": "no data available"
            }), 406)

        id = data["id"]
        if current_user and current_user['role'] == 'attendant':
            self.myproduct = ModelProduct.get(self)
            if len(self.myproduct) == 0:

                return make_response(jsonify({
                    "Message": "No products available for sale"
                }), 404)

            for product in self.myproduct:
                print(product)
                print(id)
                if product["id"] == id:
                    userid = current_user["id"]
                    mysale = ModelSales(userid, id)
                    # currentstock = data["currentstock"]
                    if int(product["currentstock"]) > 0:
                        product["currentstock"] = product["currentstock"] - 1
                    else:
                        return make_response(jsonify({
                            "Message": "sold out"
                        }), 404)


                    mysale.save(userid, id)

                    productID = id
                    update_product = ModelProduct(product)
                    update_product.update(productID)
                    new_sale = ModelSales.get_all_sales(self)
                    for sale in new_sale:
                        if product["id"] == new_sale:
                            price = int(product["price"]) * data["currentstock"]
                            total = total + price
                    if product["currentstock"] < int(product["minimumstock"]):
                        return make_response(jsonify({
                            "Message": "Alert Minimum stock reached",
                            "sales": product,
                            "total": total
                        }), 201)
                    else:
                        return make_response(jsonify({
                            "Message": "product successfully sold",
                            "sales": product,
                            "total": total
                        }), 201)

    
