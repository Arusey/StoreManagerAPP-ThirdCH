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
