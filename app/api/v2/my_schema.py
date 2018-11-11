'''predefined properties of json data'''
products_json = {
    'type': 'object',
    'maxProperties': 6,
    'properties': {
        'name': {'type': 'string'},
        'currentstock': {'type': 'string'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'price': {'type': 'string'},
        'minimumstock': {'type': 'string'},
    },
    'required': ['name', 'price', 'description',
                 'category', 'currentstock', 'minimumstock']
}

user_signup_json = {
    'type': 'object',
    'maxProperties': 4,
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'role': {'type': 'string'}
    },
    'required': ['name', 'password', 'email', 'role']
}
user_login_json = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']

}

sales_json = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'id': {'type': 'integer'},
        'currentstock': {'type': 'integer'}
    },
    'required': ['id', 'currentstock']

}

update_json = {
    'type': 'object',
    'maxProperties': 3,
    'properties': {
        'name': {'type': 'string'},
        'currentstock': {'type': 'integer'},
        'price': {'type': 'number'}
    },
    'required': ['name', 'currentstock', 'price']
}
