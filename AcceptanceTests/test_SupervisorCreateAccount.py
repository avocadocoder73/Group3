from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to create accounts for staff so that I can assign their responsibilities
"""


class SupervisorCreateAccountTest(TestCase):
    """Setup for creating accounts tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="S")
        self.temp.save()
        self.client = Client()
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """The teardown for creating accounts tests"""

    def tearDown(self):
        self.temp.delete()
        try:
            user = User.objects.get(username="test_user4")
            if user is not None:
                user.delete()
        except Exception as e:
            print(e)



    """Testing the valid creation of an account"""

    def test_ValidCreateAccount1(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test4', 'username': 'test_user4', 'password': 'PASSWORD4',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)

        self.assertEqual(resp.context['message'], "Account Created Successfully",
                         msg="Message for successful account creation failed")

    """Testing the valid creation of an account"""

    def test_ValidCreateAccount2(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test4', 'username': 'test_user4', 'password': 'PASSWORD4',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)
        self.assertEqual("test_user4", User.objects.get(username="test_user4").username,
                         msg="Account should be present in the database.")

    """Testing the invalid creation of an account"""

    def test_InvalidCreateAccount1(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD4',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)

        self.assertEqual(resp.context['message'], "Duplicate username or missing form field",
                         msg="Message for duplicate account creation failed")

    """Testing the invalid creation of an account"""

    def test_InvalidCreateAccount2(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test', 'password': 'test_user',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)

        self.assertEqual(resp.context['message'], "Duplicate username or missing form field",
                         msg="Message for missing field account creation failed")
