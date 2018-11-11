from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from instance.config import app_config
from .api.v2 import mydbblue
'''register our app in the create_app'''
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config["development"])
    app.config.from_pyfile('config.py')
    app.register_blueprint(mydbblue)

    app.config["TESTING"] = True


    return app
