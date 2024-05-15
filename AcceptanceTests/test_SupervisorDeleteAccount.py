from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to delete accounts for staff so that I can delete accounts of individuals who do not work at the school anymore
"""


class SupervisorDeleteAccountTest(TestCase):
    """Testing the setup for deleting a account"""

    def setUp(self):
        self.user = User(username="newestuser", password="newestuser2")
        self.user.save()
        self.client = Client()

    """Test deleting an account"""

    def test_deleteaccount(self):
        response = self.client.post('/account-management/',
                                    {"delusername": "newestuser", "password": "newestuser2", "status": "delete"})

        with self.assertRaises(ObjectDoesNotExist):
                User.objects.get(username="newestuser")

    """Test deleting an invalid account"""

    def test_invaliddeletion(self):
        response = self.client.post('/account-management/', {"delusername": "newestuser10", "password": "42", "status": "delete"})

        self.assertEqual(response.context['message'], "Account Deletion Failed")
