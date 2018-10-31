from flask import Flask, Blueprint
from flask_restful import Api, Resource
from .views import  AdminSignup, AdminLogin, Product, SingleProduct, Sale, AttSignup, AttLogin, SingleSale
'''creates our Blueprint'''
mydbblue = Blueprint("api", __name__, url_prefix="/api/v2")

api = Api(mydbblue)
'''includes all our routes and classes'''
api.add_resource(AdminSignup, '/auth/adminsignup')
api.add_resource(AdminLogin, '/auth/adminlogin')
api.add_resource(Product, '/products')
api.add_resource(SingleProduct, '/products/<int:id>')
api.add_resource(Sale, '/sales')
api.add_resource(SingleSale, '/sales/<saleid>')
api.add_resource(AttSignup, '/auth/attsignup')
api.add_resource(AttLogin, '/auth/login')
