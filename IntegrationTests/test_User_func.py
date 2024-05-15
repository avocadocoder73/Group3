from django.test import TestCase, Client
from TA_APP.models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions

"""Testing the User_func class methods integrating together"""


class UserTests(TestCase):
    """Setup for User_func tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st Street", type="TA")
        self.temp.save()
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="I")
        self.temp3.save()

    """Tear down for User_func tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp3.delete()

    """Test creating a user and finding it in the database"""

    def test_create_user_1(self):
        test_dic = {'name': 'Test4', 'username': 'test_user4', 'password': 'PASSWORD4',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    'skills': ''}
        test_list = [test_dic]
        functions.User_func.Create(self, info=test_dic)
        self.assertEqual(test_list, functions.User_func.get(self, query='username', identity='test_user4'),
                         msg="User not found")
        temp_user = User.objects.get(username="test_user4")
        temp_user.delete()

    """Test editing a current user and getting it from the database"""

    def test_edit_user_info_1(self):
        test_dic = {'username': 'test_user', 'name': 'New-Test'}
        new_list = [{'name': 'New-Test', 'username': 'test_user', 'password': 'PASSWORD',
                     'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                     'skills': ''}]
        functions.User_func.Edit(self, info=test_dic)
        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user"),
                         msg="User information not updated")

    """Test editing a current user and getting it from the database"""

    def test_edit_user_info_2(self):
        test_dic = {'username': 'test_user', 'name': 'New-Test', 'address': '321 1st Street'}
        new_list = [{'name': 'New-Test', 'username': 'test_user', 'password': 'PASSWORD',
                     'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '321 1st Street', "type": "TA",
                     'skills': ''}]
        functions.User_func.Edit(self, info=test_dic)
        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user"),
                         msg="User information not updated")

    """Test deleting a user and checking if it exist"""

    def test_delete_user_1(self):
        functions.User_func.Delete(self, identity='test_user')
        self.assertEqual([], functions.User_func.get(self, query="username", identity='test_user'),
                         "User should not exist in the database")