from .BaseTest import *

class TestProducts(TestAllEndpoints):
    def test_post_products(self):
        response = self.test_client.post("/api/v2/products",
                                         data=json.dumps({
                                            "name": "coffee",
                                            "category": "junk",
                                            "description": "super delicious",
                                            "currentstock": 23,
                                            "minimumstock": 2,
                                            "price": 200
                                         }),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "Product posted successfully")
        self.assertEqual(response.status_code, 201)
    def test_get_all_products(self):
        response = self.test_client.get("/api/v2/products",
                                         data=self.product,
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)

        self.assertEqual(message["Message"], "All products fetched successfully")
        self.assertEqual(response.status_code, 200)

    def test_get_single_products(self):
        response = self.test_client.get("/api/v2/products/1",
                                         data=self.product,
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "Product retrieval successful")
        self.assertEqual(response.status_code, 200)
    def test_delete_product(self):
        response = self.test_client.delete("/api/v2/products/1",
                                         data=self.product,
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["message"], "Deleted successfully")
        self.assertEqual(response.status_code, 200)

    def test_delete_product_in_sales(self):
        response = self.test_client.delete("/api/v2/products/6",
                                            data=self.product,
                                            headers={
                                                'content-type': 'application/json',
                                                'x-access-token': self.token_for_admin
                                            })
        message = json.loads(response.data)
        self.assertEqual(message["Message"], "The product selected for deletion does not exist")
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        response = self.test_client.put("/api/v2/products/1",
                                         data=json.dumps(
                                            {
                                               "name": "burger",
                                               "currentstock": 23,
                                               "price": 200
                                            }
                                         ),
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        print(response.data)
        self.assertEqual(message["Message"], "product has been updated successfully")
        self.assertEqual(response.status_code, 200)
    def test_empty_products(self):
        response = self.test_client.post("/api/v2/products",
                                         data=json.dumps({
                                             "name": "",
                                             "category": "",
                                             "description": "",
                                             "currentstock": "",
                                             "minimumstock": "",
                                             "price": ""
                                         }),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "u'' is not of type 'number'")
        self.assertEqual(response.status_code, 400)

    def test_missing_key(self):
        response = self.test_client.post("/api/v2/products",
                                         data=json.dumps({
                                             "": "malenge",
                                             "": "food",
                                             "": "good food",
                                             "": 123,
                                             "": 3,
                                             "": 400
                                         }),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "'name' is a required property")
        self.assertEqual(response.status_code, 400)

    def test_product_registered(self):
        response = self.test_client.post("/api/v2/products",
                                         data=self.product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Product already registered")
        self.assertEqual(response.status_code, 406)

    def test_space_in_data(self):
        response  = self.test_client.post("/api/v2/products",
                                         data=json.dumps({
                                             "name": "njugu ",
                                            "category": "junk ",
                                            "description": "super delicious",
                                            "currentstock": 23,
                                            "minimumstock": 2,
                                            "price": 200
                                         }),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token_for_admin
                                         })
        message = json.loads(response.data)
        self.assertEqual(message["message"], "Ensure no spaces when entering detail")
        self.assertEqual(response.status_code, 400)
