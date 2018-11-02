from .BaseTest import *

class TestMyUsers(TestAllEndpoints):
    def test_user_signup(self):
        '''tests for a full signup'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "hezz",
                                            "email": "hezz@email.com",
                                            "password": "Hezz@123",
                                            "role": "attendant"
                                         }),
                                         headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["Message"], "user successfully registered")
        self.assertEqual(response.status_code, 201)
    def test_user_exists(self):
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=self.attendant,
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["message"], "User already exists")
        self.assertEqual(response.status_code, 406)

    def test_missing_data(self):
        '''test for missing email'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "",
                                            "email": "",
                                            "password": "",
                                            "role": ""
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Missing credentials, check again")
        self.assertEqual(response.status_code, 400)

    def test_signup_datatype(self):
        '''test whether the correct datatype has been inserted'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": 371979,
                                            "email": 327487,
                                            "password": 7293,
                                            "role": 394923
                                         }), headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "7293 is not of type 'string'")
        self.assertEqual(response.status_code, 400)

    def test_valid_email(self):
        '''test whether the email is valid'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "blah",
                                            "email": "fijkwej",
                                            "password": "Blah@123",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["message"], "The email is not valid")
        self.assertEqual(response.status_code, 400)
    def test_password_length(self):
        '''test for the length of password'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "brad",
                                            "email": "brad@email.com",
                                            "password": "k@12",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Password must be long than 6 characters or less than 12")
        self.assertEqual(response.status_code, 400)

    def test_password_isdigit(self):
        '''test whether there is a digit in password'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "pitt",
                                            "email": "pitt@email.com",
                                            "password": "dwifiwf",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Password must have a digit")
        self.assertEqual(response.status_code, 400)

    def test_password_uppercase(self):
        '''test whether password has uppercase'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "pratt",
                                            "email": "pratt@email.com",
                                            "password": "dwifiwf@34",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Password must have an upper case character")
        self.assertEqual(response.status_code, 400)
    def test_password_lowercase(self):
        '''test whether password has lowercase'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "chris",
                                            "email": "chris@email.com",
                                            "password": "JBFJE@34",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Password must have a lower case character")
        self.assertEqual(response.status_code, 400)

    def test_password_specialchar(self):
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "meg",
                                            "email": "meg@email.com",
                                            "password": "JBFwdJE34",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Password must have a special charater")
        self.assertEqual(response.status_code, 400)

    def test_space_in_name(self):
        '''test whether there is a space in name'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "ones ",
                                            "email": "ones@email.com",
                                            "password": "Ones@123",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Remove space in name")
        self.assertEqual(response.status_code, 400)
    def test_space_in_email(self):
        '''test whether there is a space in name'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "ones",
                                            "email": "ones@email.com ",
                                            "password": "Ones@123",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Remove space in email")
        self.assertEqual(response.status_code, 400)
    def test_space_in_password(self):
        '''test whether there is a space in password'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "ones",
                                            "email": "ones@email.com",
                                            "password": "Ones@123 ",
                                            "role": "attendant"
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Remove space in password")
        self.assertEqual(response.status_code, 400)

    def test_space_in_role(self):
        '''test whether there is a space in name'''
        response = self.test_client.post("/api/v2/auth/attsignup",
                                         data=json.dumps({
                                            "name": "ones",
                                            "email": "ones@email.com",
                                            "password": "Ones@123",
                                            "role": "attendant "
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["message"], "Remove space in role")
        self.assertEqual(response.status_code, 400)

    def test_admin_login(self):
        '''test for a successful login'''
        response = self.test_client.post("/api/v2/auth/adminlogin",
                                         data=self.admin_login,
                                         headers={
                                         'content-type': 'application/json',

                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "user successfully logged in")
        self.assertEqual(response.status_code, 200)

    def test_wrong_details(self):
        response = self.test_client.post("/api/v2/auth/adminlogin",
                                         data=json.dumps({
                                            "email": "winner@email.com",
                                            "password": "Blah@email.com"
                                         }),
                                         headers={
                                         'content-type': 'application/json'
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "Login failed, wrong entries")
        self.assertEqual(response.status_code, 403)



    def test_attendant_login(self):
        '''test for when attendant logs in'''
        response = self.test_client.post("/api/v2/auth/login",
                                         data=self.attendant_login,
                                         headers={
                                            'content-type': 'application/json'
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "user successfully logged in")
        self.assertEqual(response.status_code, 200)
    def test_wrong_entries(self):
        response = self.test_client.post("/api/v2/auth/adminlogin",
                                         data=json.dumps({
                                            "email": "mercy@email.com",
                                            "password": "Loco@123"
                                         }),
                                         headers={
                                            'content-type': 'application/json'
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["Message"], "Login failed, wrong entries")
        self.assertEqual(response.status_code, 403)


    def test_logout_user(self):
        pass
