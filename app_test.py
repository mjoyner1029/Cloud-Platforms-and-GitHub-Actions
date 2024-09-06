# app_test.py

import unittest
from app import app, db, Sum

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_add_sum(self):
        response = self.app.post('/sum', json={'a': 3, 'b': 5})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['a'], 3)
        self.assertEqual(data['b'], 5)
        self.assertEqual(data['result'], 8)

    def test_get_sums_by_result(self):
        # Add some sums to the database
        db.session.add(Sum(a=1, b=3, result=4))
        db.session.add(Sum(a=2, b=2, result=4))
        db.session.commit()

        response = self.app.get('/sum/result/4')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['a'], 1)
        self.assertEqual(data[0]['b'], 3)
        self.assertEqual(data[0]['result'], 4)
        self.assertEqual(data[1]['a'], 2)
        self.assertEqual(data[1]['b'], 2)
        self.assertEqual(data[1]['result'], 4)

    def test_get_sums_by_result_invalid(self):
        response = self.app.get('/sum/result/999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

if __name__ == '__main__':
    unittest.main()
