from .BaseTest import *

class TestSales(TestAllEndpoints):
    def test_post_sale(self):
        response = self.test_client.post("api/v2/sales",
                                         data=json.dumps(
                                             {
                                                 "id": 1,
                                                 "currentstock": 5
                                             }
                                         ),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_attendant
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "product successfully sold")
        self.assertEqual(response.status_code, 201) 

    def test_no_product(self):
        response = self.test_client.post("api/v2/sales",
                                         data=json.dumps(
                                             {
                                                 "id": 1000,
                                                 "currentstock": 3
                                             }
                                         ), 
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_attendant
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["Message"], "this product does not exist")
        self.assertEqual(response.status_code, 404)

    def test_minimumstock(self):
        response = self.test_client.post("api/v2/sales",
                                         data=json.dumps(
                                             {
                                                 "id": 1,
                                                 "currentstock": 22
                                             }
                                         ), 
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_attendant
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "Alert Minimum stock reached")
        self.assertEqual(response.status_code, 201)
        
        
                    