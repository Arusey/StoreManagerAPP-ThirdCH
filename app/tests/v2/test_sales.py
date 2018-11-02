# from .BaseTest import *

<<<<<<< HEAD
class TestSales(TestAllEndpoints):
    """test whether whther all sales are retrieved successfully"""
    def test_sale_success(self):
        response = self.test_client.post("/api/v2/sales",
                                         data=self.sale,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_attendant
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "product successfully sold")
        self.assertEqual(response.status_code, 201)
=======
# class TestSales(TestAllEndpoints):
#     """test whether whther all sales are retrieved successfully"""
#     def test_sale_success(self):
#         response = self.test_client.post("/api/v2/sales",
#                                          data=self.sale,
#                                          headers={
#                                              'content-type': 'application/json',
#                                              'x-access-token': self.token_for_attendant
#                                          })
#         message = json.loads(response.data)
#         self.assertEqual(message["message"], "product successfully sold")
#         self.assertEqual(response.status_code, 201)
>>>>>>> 261443fc38d602bfb6eb3e54573a13e552f15bdd

#     def test_empty_sale_data(self):
#         """test whether empty data is inserted in sales endpoint"""
#         response = self.test_client.post("/api/v2/sales",
#                                          data=json.dumps({

<<<<<<< HEAD
                                         }),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_attendant
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "no data available")
        self.assertEqual(response.status_code, 406)
=======
#                                          }),
#                                          headers={
#                                              'content-type': 'application/json',
#                                              'x-access-token': self.token_for_attendant
#                                          })
#         message = json.loads(response.data)
#         self.assertEqual(message["message"], "no data available")
#         self.assertEqual(response.status_code, 406)
>>>>>>> 261443fc38d602bfb6eb3e54573a13e552f15bdd

#     def test_get_all_sales(self):
#         """test whether all sales have been retrieved"""
#         response = self.test_client.get("/api/v2/sales",
#                                          data=self.sale,
#                                          headers={
#                                              'content-type': 'application/json',
#                                              'x-access-token': self.token_for_admin
#                                          })
#         message = json.loads(response.data)
#         self.assertEqual(message["Message"], "sale retrieval is successful")
#         self.assertEqual(response.status_code, 200)
