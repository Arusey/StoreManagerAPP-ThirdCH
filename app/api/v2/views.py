from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import Config
from flask_expects_json import expects_json
import jwt
import datetime

from .my_schema import *
from .models.userModel import UserModel
from .models.databaseModel import Db
from .models.productsModel import ModelProduct
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
            db = Db()
            conn = db.create_connection()
            db.create_tables()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM badtokens WHERE token = %s", (token,)
            )
            if cursor.fetchone():
                return make_response(jsonify({
                    "Message": "Token has been invalidated, kindly login"
                }), 403)
        if not token:
            return make_response(jsonify({
                                 "Message": "the access token is missing, Login"}, 401))
        try:
            data = jwt.decode(
               token, Config.SECRET_KEY, algorithms=['HS256'])
            print(data)
            newuser = UserModel()
            users = newuser.getusers()
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



class AttSignup(Resource):
    """docstring for attendant Signup."""
    @token_required
    @expects_json(user_signup_json)
    def post(current_user, self):

        data = request.get_json()
        valid = AuthValidate(data)
        valid.validate_invalid_entry(data)
        valid.validate_empty_data(data)
        valid.validate_details(data)
        if current_user and current_user["role"] == "admin":

            name = data["name"].lower()
            email = data["email"].lower()
            password = data["password"]
            role = data["role"].lower()
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
    @token_required
    def get(current_user, self):
        '''docstring for getting all users'''
        if current_user and current_user["role"] == "admin":
            user = UserModel()
            users = user.getusers()
            return make_response(jsonify({
                "Message": "all users retrieved successfully",
                "users": users
            }
            ), 200)
        return make_response(jsonify({
            "Message": "Please login first"
        }), 401)


class AdminLogin(Resource):
    '''docstring for administrator login'''
    @expects_json(user_login_json)
    def post(self):
        '''login as user and encode a jwt token'''
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        user_obj = UserModel()
        users = user_obj.getusers()
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
    @expects_json(user_login_json)
    def post(self):
        '''login as attendant and encode a jwt token'''
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        myuser = UserModel()
        users = myuser.getusers()
        for user in users:
            print(user)

            print(user["email"])
            print(email)
            print(password, user["password"])
            if email == user["email"] and password == user["password"]:
                print(user, "idjscijk")
                token = jwt.encode({
                "email": email,
                "password" : password,
                "exp": datetime.datetime.utcnow() + datetime.timedelta
                                                (minutes=54567)
                }, Config.SECRET_KEY, algorithm='HS256')
                return make_response(jsonify({
                            "Message": "user successfully logged in",
						     "token": token.decode("UTF-8")}), 200)
        return make_response(jsonify({
            "Message": "Login failed, wrong entries"
        }
        ), 403)







class Product(Resource):
    @token_required
    @expects_json(products_json)
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
        pvalid = ProductValidate(data=data)
        pvalid.validate_empty_products()
        pvalid.validate_products_data()


        name = data["name"].lower()
        category = data["category"].lower()
        description = data["description"].lower()
        currentstock = int(data["currentstock"])
        minimumstock = int(data["minimumstock"])
        price = int(data["price"])

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
class SingleProduct(Resource):
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
    @token_required
    def delete(current_user, self, id):
        '''deletes a selected product'''
        product = ModelProduct()
        products = product.get()
        mysales = ModelSales()
        sales = mysales.get_all_sales()
        if current_user["role"] != "admin":
            return make_response(jsonify({
                "Message": "You have no authorization to delete a product"
            }), 403)
        for item in products:
            if item["id"] in sales:
                return make_response(jsonify({
                    "Message": "Product in sales, You cannot delete"
                }), 403)
            if id == item["id"]:
                product.delete(id)
                message = make_response(jsonify({
                    "message": "Deleted successfully"
                }), 200)
                return message
        message = make_response(jsonify({
            "Message": "The product selected for deletion does not exist"
        }))

        return message

    @token_required
    @expects_json(update_json)
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
                    if int(product["currentstock"]) > 0:
                        product["currentstock"] = product["currentstock"] - data["currentstock"]
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
            return make_response(jsonify({
                "Message": "this product does not exist"
            }), 404)



    @token_required
    def get(current_user, self):
        '''getting all sales made'''
        if current_user and current_user["role"] == "admin":
            saleitem = ModelSales()
            sales = saleitem.get_all_sales()

            if sales:
                return make_response(jsonify({
                    "Message": "sale retrieval is successful",
                    "sales": sales
                }), 200)
            else:
                return make_response(jsonify({
                    "Message": "unfortunately no sale has been made"
                }), 404)
        else:
            return make_response(jsonify({
                "Message": "viewing sales is reserved for the admin",

            }), 401)


class SingleSale(Resource):
    @token_required
    def get(current_user, self, saleid):
        if current_user:
            saleitem = ModelSales()
            sales = saleitem.get_all_sales()
            if not sales:
                return make_response(jsonify({
                            "Message": "No available sales"
                        }), 404)
            for singlesale in sales:
                if int(saleid)  == int(singlesale["saleid"]):
                    print(saleid)
                    return make_response(jsonify({
                        "Message": "Sale  retrieval is successful",
                        "sale": singlesale
                    }), 200)


class Logout(Resource):
    @token_required
    def post(current_user, self):
        try:
            if current_user:
                if 'x-access-token' in request.headers:
                    token = request.headers["x-access-token"]
                    thisuser = UserModel()
                    date = datetime.datetime.now()
                    thisuser.user_logout(token, date)
                    return make_response(jsonify({
                        "Message": "Log out, see you later"
                    }), 200)
        except Exception as e:
            return make_response(jsonify({
                "Message": "Failed to blacklist token"
            }), 403)
