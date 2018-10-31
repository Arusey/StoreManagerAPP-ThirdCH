import os

class Config():

    debug = False
    SECRET_KEY = "secretkey"
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    APP_SETTINGS = os.getenv("APP_SETTINGS")

class Develop(Config):
    """Configuration for the development enviroment"""
    debug = True


class Testing(Config):
    """Configuration for the testing enviroment"""
    WTF_CSRF_ENABLED = False
    debug = True


app_config={
"development": Develop,
"testing": Testing
}
