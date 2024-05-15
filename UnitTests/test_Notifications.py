from django.test import TestCase, Client
from TA_APP.models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions

"""Test notification low level functions"""

class NotificationsTests(TestCase):
    """Setup for notify tests"""
    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="I")
        self.temp.save()
        self.temp2 = User(name="Test2", username="test_user2", password="PASSWORD2", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st Street", type="TA")
        self.temp2.save()
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="S")
        self.temp3.save()

    """Teardown for notify tests"""
    def tearDown(self):
        self.temp.delete()
        self.temp2.delete()
        self.temp3.delete()

    """Testing the valid email file"""
    def test_valid_email_1(self):
        filename = "valid_email_1.txt"
        self.assertTrue(functions.Notify.email(self,filename))

    """Testing the valid email file"""
    def test_valid_email_2(self):
        filename = "valid_email_2.txt"
        self.assertTrue(functions.Notify.email(self,filename))

    """Testing the valid email file"""
    def test_valid_email_3(self):
        filename = "valid_email_3.txt"
        self.assertTrue(functions.Notify.email(self,filename))

    """Testing the invalid email file"""
    def test_invalid_email_1(self):
        filename = "invalid_email_1.txt"
        self.assertTrue(functions.Notify.email(self,filename))

    """Testing the invalid email file"""
    def test_invalid_email_2(self):
        filename = "invalid_email_2.txt"
        self.assertTrue(functions.Notify.email(self,filename))

    """Testing the invalid email file"""
    def test_invalid_email_3(self):
        filename = "invalid_email_3.txt"
        self.assertTrue(functions.Notify.email(self,filename))
