from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a Supervisor, Instructor, TA I want to edit my own contact information, so that students and staff my reach me.
"""


class EditContactInformation(TestCase):
    """Setup for edit contact info tests"""

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

    """Teardown for edit contact info tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp2.delete()
        self.temp3.delete()

    """Testing if a supervisor can edit their own contact info"""

    def test_edit_contact_supervisor(self):
        session = self.client.session
        session['username'] = 'test_user3'
        session.save()

        new_list = [{'name': 'Test3', 'username': 'test_user3', 'password': 'PASSWORD3',
                     'email': 'test3@uwm.edu', 'phone_number': 4567892122, 'address': '123 1st Street', "type": "S",'skills': ''}]

        response = self.client.post('/editcontactinfo/',
                                    {
                                     'email': 'test3@uwm.edu', 'phone': "4567892122",
                                     'address': '123 1st Street', "status": "edit_contact"},
                                    follow=True)


        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user3"))

    """Testing if a supervisor can edit their own contact info"""

    def test_edit_contact_instructor(self):
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

        new_list = [{'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                     'email': 'test6@uwm.edu', 'phone_number': 4327537522, 'address': '123 3rd Street', "type": "I",
                     'skills': ''}]

        response = self.client.post('/editcontactinfo/',
                                    {'email': 'test6@uwm.edu', 'phone': "4327537522",
                                     'address': '123 3rd Street'},
                                    follow=True)

        print(functions.User_func.get(self, query="username", identity="test_user"))

        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user"))

    """Testing if a TA can edit their own contact info including their skills information"""

    def test_edit_contact_TA(self):
        session = self.client.session
        session['username'] = 'test_user2'
        session.save()

        new_list = [{'name': 'Test2', 'username': 'test_user2', 'password': 'PASSWORD2',
                     'email': 'test5@uwm.edu', 'phone_number': 3123543444, 'address': '123 1st Street', "type": "TA",
                     'skills': ''}]

        response = self.client.post('/editcontactinfo/',
                                    {
                                     'email': 'test5@uwm.edu', 'phone': "3123543444",
                                     'address': '123 1st Street'},
                                    follow=True)



        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user2"))
