# StoreManagerAPP-ThirdCH
[![Build Status](https://travis-ci.com/Arusey/StoreManagerAPP-ThirdCH.svg?branch=develop)](https://travis-ci.com/Arusey/StoreManagerAPP-ThirdCH)
[![Coverage Status](https://coveralls.io/repos/github/Arusey/StoreManagerAPP-ThirdCH/badge.svg?branch=develop)](https://coveralls.io/github/Arusey/StoreManagerAPP-ThirdCH?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/b4e9e82c81b8959c52cc/maintainability)](https://codeclimate.com/github/Arusey/StoreManagerAPP-ThirdCH/maintainability)


This is application for managing sales in a given store
App Description
===============
This is a store manager application that allows the stakeholders of a given store to perform actions such as:
* Sign up to the application
* Login to the application
* Post a product
* Post a Sale
* Get all products
* Get single product
* Get all products
* Get all sales
* Get single sale

Installation
============

Take the following steps:
1. Create a virtual enviroment with the command `$ virtualenv -p python3 env`
1. Activate the virtual enviroment with the command `$ source env/bin/activate`
1. Ensure you have installed GIT
1. Clone the repository i.e `$ git clone https://github.com/Arusey/StoreManagerAPP-ThirdCH`
1. Install requirements `$ pip install -r requirements.txt`

Documentation
=============

Heroku Deploy
=============


Running Tests
=============
After completing the following, it is time to run the app
1. To run the tests use `$ pytest -v`
1. To run the application use `export SECRET_KEY="<your secret key>"`
1. `export FLASK_APP=run.py'
1. `flask run`

The following endpoints should be working:

|Endpoint|functionality|contraints(requirements)|
|-------|-------------|----------|
|post /api/v2/auth/attsignup|create a user|user information|
|post /api/v2/auth/login | login |requires authentication |
|get /api/v2/products| get all the products| pass a token |
|get /api/v2/products/<int:id>|return a single product| product id, pass token|
|post /api/v2/products | create a new product entry| product data, pass token|
|post /api/v2/sales | create a new sale| product id, pass token|
|get /api/v2/sales | get all sales entries| pass token|
|get/api/v2/sales/<saleid>|get a single sale entry| sale id, pass token|ad
|delete/api/v2/products/<int:id> | delete a product | product id, pass token
|update/api/v2/products/<int:id> | update a product | product id, pass token


 Technologies used include:
 ==========================
 * Python
 * Flask
 * Flask-Restful
 * Json Web Tokens
 * Heroku
 * Travis CI
 * Coveralls
 * Code Climate

 Acknowldegments
 ===============
 I would like to acknowledge the Andela Bootcamp 33 for facilitating this project
