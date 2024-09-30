import json
from api.utils.test_base import BaseTestCase
from api.models.users import User
from datetime import datetime
import unittest2 as unittest
from api.utils.token import generate_verification_token, confirm_verification_token

# method to create users using model to facilitate testing
def create_users():
    user1 = User(email="george@gmail.com", first_name='George', last_name='Okudo',
    password_hash=User.generate_hash('abc$'), isVerified=True).create()

    user2 = User(email="zonicah@gmail.com",
    first_name='Zonicah', last_name='Ochieng',
    password_hash=User.generate_hash('abc')).create()

# Class to hold all tests
class TestUsers(BaseTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
    create_users()

    def test_login_user(self):
        user = {
            "email" : "george@gmail.com",
            "first_name": "George",
            "last_name": "Okudo",
            "password_hash": "abc$"
        }
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in data)

if __name__ == '__main__':
    unittest.main()
        