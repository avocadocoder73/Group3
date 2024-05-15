from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to see all users and all their personal information so that I can have detailed records of staff.
PBI: As a Instructor, TA I would like to see all users so that I can see all of the staff in my department.
"""


class ViewUsers(TestCase):
    """setup for viewusers tests"""

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
        self.client = Client()

    """Teardown for view users info tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp2.delete()
        self.temp3.delete()

    """Test viewing all the users on the page"""

    def test_viewusers(self):
        """Set session"""
        session = self.client.session
        session['username'] = 'test_user3'
        session.save()

        response = self.client.get('/view-users/')



        # Check that we get a response
        self.assertEqual(response.status_code, 200)

        # check the context for the lists for courses
        self.assertEqual(functions.User_func.get_all(self), response.context['users'],
                         msg="View Courses should have all the information when get request is given")
