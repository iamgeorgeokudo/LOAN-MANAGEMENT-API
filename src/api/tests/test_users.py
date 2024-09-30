import json
from api.utils.test_base import BaseTestCase
from api.models.users import User
from datetime import datetime
import unittest2 as unittest
from api.utils.token import generate_verification_token, confirm_verification_token

