from django.test import TestCase, Client
from TA_APP.models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions

"""Testing the login class"""


class LoginTest(TestCase):
    """Setup for authentication tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="I")
        self.temp.save()
        self.temp2 = User(name="Test2", username="test_user2", password="PASSWORD2", email="test@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="T")
        self.temp2.save()
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="S")
        self.temp3.save()

    """Teardown for authentication tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp2.delete()
        self.temp3.delete()

    """Test a valid instructor logging in"""

    def test_login_1(self):
        self.assertEqual("I", functions.Login.authenticate(self, username="test_user", password="PASSWORD"),
                         msg="User exists should return true")

    """Test a valid TA logging in"""

    def test_login_2(self):
        self.assertEqual("T", functions.Login.authenticate(self, username="test_user2", password="PASSWORD2"),
                         msg="User exists should return true")

    """Test an valid Supervisor logging in"""

    def test_login_3(self):
        self.assertEqual("S", functions.Login.authenticate(self, username="test_user3", password="PASSWORD3"),
                         msg="User exists should return true")

    """Test an invalid password"""

    def test_login_4(self):
        self.assertEqual("Invalid password", functions.Login.authenticate(self, username="test_user", password="WORD"),
                         msg="Wrong password should return false")

    """Test an invalid username"""

    def test_login_5(self):
        self.assertEqual("No such user", functions.Login.authenticate(self, username="test_user5", password="WORD"),
                         msg="Wrong user should return false")
