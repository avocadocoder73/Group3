from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a user I would like to be able to sign into my account so that I can access it securely
"""


class LoginTest(TestCase):
    """The setpUp for LoginTests"""

    def setUp(self):
        self.user = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="S")
        self.user.save()
        self.client = Client()

    """Teardown for login tests"""

    def tearDown(self):
        self.user.delete()

    """Testing the valid login information"""

    def test_validLogin(self):
        response = self.client.post("/", {"username": "test_user", "password": "PASSWORD"})
        ##routes to homepage if valid

        self.assertEqual(response.context['status'], "Signed In")

    """Testing the login with invalid username and password"""

    def test_invalidLogin(self):
        response = self.client.post("/", {"username": "test_user42", "password": "PASSWORD123"})



        ##if html contains message that username or password is incorrect creds are invalid
        self.assertEqual(response.context['message'], 'Username or password is incorrect')
