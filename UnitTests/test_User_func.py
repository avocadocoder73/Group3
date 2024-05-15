from django.test import TestCase, Client
from TA_APP.models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions

"""Testing the User_func class"""


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

    """Test getting the user based on the username"""

    def test_get_user_info_1(self):
        test_dic = {'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    "skills": ''}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.User_func.get(self, query='username', identity='test_user'),
                         msg="User not found")

    """Test getting the user based on the name"""

    def test_get_user_info_2(self):
        test_dic = {'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    "skills": ''}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.User_func.get(self, query='name', identity='Test'), msg="User not found")

    """Test getting the user based on the password"""

    def test_get_user_info_3(self):
        test_dic = {'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    "skills": ''}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.User_func.get(self, query='password', identity='PASSWORD'),
                         msg="User not found")

    """Test getting the user based on the email"""

    def test_get_user_info_4(self):
        test_dic = {'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    "skills": ''}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.User_func.get(self, query='email', identity='test@uwm.edu'),
                         msg="User not found")

    """Test getting the user based on the phone number"""

    def test_get_user_info_5(self):
        test_list = [{'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                      'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', 'type': "TA",
                      'skills': ''},
                     {'name': 'Test3', 'username': 'test_user3', 'password': 'PASSWORD3',
                      'email': 'test3@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', 'type': "I",
                      'skills': ''}]
        self.assertEqual(test_list, functions.User_func.get(self, query='phone_number', identity=str(1234567890)),
                         msg="User not found")

    """Test getting the user based on the address"""

    def test_get_user_info_6(self):
        test_list = [{'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                      'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', 'type': "TA",
                      'skills': ''},
                     {'name': 'Test3', 'username': 'test_user3', 'password': 'PASSWORD3',
                      'email': 'test3@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', 'type': "I",
                      'skills': ''}]
        self.assertEqual(test_list, functions.User_func.get(self, query='address', identity='123 1st Street'),
                         msg="User not found")

    """Test getting the user based on type"""

    def test_get_user_info_7(self):
        test_dic = {'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    'skills': ''}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.User_func.get(self, query="type", identity="TA"), msg="User not found")

    """Test getting a user that does not exist"""

    def test_get_user_info_8(self):
        self.assertEqual([], functions.User_func.get(self, query="username", identity="test_user2"),
                         msg="User not found")

    """Test getting all users in the database"""

    def test_get_all_users(self):
        test_list = [{'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                      'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', 'type': "TA",
                      'skills': ''},
                     {'name': 'Test3', 'username': 'test_user3', 'password': 'PASSWORD3',
                      'email': 'test3@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', 'type': "I",
                      'skills': ''}]
        self.assertEqual(test_list, functions.User_func.get_all(self),
                         msg="List of users not found in database when they should be")

    """Test creating a valid user"""

    def test_create_user_1(self):
        test_dic = {'name': 'Test4', 'username': 'test_user4', 'password': 'PASSWORD4',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA"}
        self.assertEqual(True, functions.User_func.Create(self, info=test_dic),
                         msg="Operation should have been successful")
        temp_user = User.objects.get(username="test_user4")
        temp_user.delete()

    """Test creating a valid user"""

    def test_create_user_2(self):
        test_dic = {'name': 'Test4', 'username': 'test_user4', 'password': 'PASSWORD4',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    'skills': 'HTML'}
        self.assertEqual(True, functions.User_func.Create(self, info=test_dic),
                         msg="Operation should have been successful")
        temp_user = User.objects.get(username="test_user4")
        temp_user.delete()

    """Test creating a user with an invalid dictionary"""

    def test_create_user_3(self):
        test_dic = {'name': 'Test4', 'username': 'test_user4'}
        self.assertEqual(False, functions.User_func.Create(self, info=test_dic),
                         msg="Incorrect dictionary operation is should be unsuccessful")

    """Test creating a user with an invalid empty dictionary"""

    def test_create_user_4(self):
        test_dic = {}
        self.assertEqual(False, functions.User_func.Create(self, info=test_dic),
                         msg="Empty dictionary operation is unsuccessful")

    """Test creating a duplicate user"""

    def test_create_user_5(self):
        test_dic = {'name': 'Test4', 'username': 'test_user', 'password': 'PASSWORD4',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street', "type": "TA",
                    'skills': 'HTML'}
        self.assertEqual(False, functions.User_func.Create(self, info=test_dic),
                         msg="Operation should have been successful cannot have repeated usernames")

    """Test editing a valid user"""

    def test_edit_user_info_1(self):
        test_dic = {'username': 'test_user', 'name': 'New-Test'}
        self.assertEqual(True, functions.User_func.Edit(self, info=test_dic),
                         msg="Should return true because user exist")

    """Test editing a user with the wrong input"""

    def test_edit_user_info_2(self):
        test_dic = {}
        self.assertEqual(False, functions.User_func.Edit(self, info=test_dic),
                         msg="Should return false because input dictionary does not exist")

    """Test editing a user with an invalid user"""

    def test_edit_user_info_3(self):
        test_dic = {'username': 'test_user17', 'name': 'New-Test'}
        self.assertEqual(False, functions.User_func.Edit(self, info=test_dic),
                         msg="Should return false because user does not exist")

    """Test editing a user without the required username information"""

    def test_edit_user_info_4(self):
        test_dic = {'name': 'New-Test'}
        self.assertEqual(False, functions.User_func.Edit(self, info=test_dic),
                         msg="Should return false because username is required")

    """Test deleting a user"""

    def test_delete_user_1(self):
        self.assertEqual(True, functions.User_func.Delete(self, identity='test_user'),
                         "User should successfully delete")

    """Test deleting a user that does not exist"""

    def test_delete_user_2(self):
        self.assertEqual(False, functions.User_func.Delete(self, identity='test_user81'),
                         "User should not exist in the database")


