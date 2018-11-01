from flask import Flask, Blueprint
from flask_restful import Api, Resource
from .views import  AdminLogin, Product, SingleProduct, AttSignup, AttLogin
'''creates our Blueprint'''
mydbblue = Blueprint("api", __name__, url_prefix="/api/v2")

api = Api(mydbblue)
'''includes all our routes and classes'''
api.add_resource(AdminLogin, '/auth/adminlogin')
api.add_resource(Product, '/products')
api.add_resource(SingleProduct, '/products/<int:id>')
api.add_resource(AttSignup, '/auth/attsignup')
api.add_resource(AttLogin, '/auth/login')
