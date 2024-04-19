from django.test import TestCase, Client
from .models import User, Instructor, TA, Course, LabSection
import TA_APP.functions as functions


class UserTests(TestCase):

    def setUp(self):
        temp = User(user_id=1, name="Test", password="PASSWORD", email="test@uwm.edu",
                    phone_number=1234567890, address="123 1st street")
        temp.save()

    def test_get_user_info_1(self):
        test_dic = {'user_id': 1, 'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                    'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street'}
        self.assertEqual(test_dic, functions.User.get_user_info(self,user_id=1), msg="User not found")

    def test_get_user_info_2(self):
        self.assertEqual({}, functions.User.get_user_info(self,user_id=2), msg="User not found")

    def test_update_user_info_1(self):
        test_dic = {'user_id': 1, 'name': 'New-Test'}
        new_dic = {'user_id': 1, 'name': 'New-Test', 'username': 'test_user', 'password': 'PASSWORD',
                   'email': 'test@uwm.edu', 'phone_number': 1234567890, 'address': '123 1st Street'}
        functions.User.update_user_info(self,test_dic)
        self.assertEqual(new_dic, functions.User.get_user_info(self,user_id=1), msg="User information not updated")

    def test_update_user_info_2(self):
        test_dic = {'user_id': 1, 'name': 'New-Test'}
        self.assertEqual(True, functions.User.update_user_info(self,info=test_dic),
                         msg="Should return true becuase user exist")

    def test_update_user_info_3(self):
        test_dic = {}
        self.assertEqual(False, functions.User.update_user_info(self,info=test_dic),
                         msg="Should return false becuase input dictionary does not exist")

    def test_update_user_info_4(self):
        test_dic = {'user_id': 2, 'name': 'New-test'}
        self.assertEqual(False, functions.User.update_user_info(self,info=test_dic),
                         msg="Should return false becuase user does not exist")

    def test_delete_user_1(self):
        self.assertEqual(True,functions.User.delete_user(self,user_id=1),"User should succefully delete")

    def test_delete_user_2(self):
        self.assertEqual(False,functions.User.delete_user(self,user_id=2),"User should not exist in the database")


class CourseTests(TestCase):

    def setUp(self):
        user = User(user_id=1, name="Test",password="PASSWORD", email="test@uwm.edu",
                    phone_number=1234567890, address="123 1st street")
        instructor = Instructor(user_id=user,instructor_id=1)
        temp = Course(course_id="11111", course_name="Test Course",course_code=101)

    def test_get_course_info_1(self):
        test_dic = {'course_id': '11111', 'course_name': 'Test Course', 'course_code':101}
        self.assertEqual(test_dic, functions.Course.get_course_info(self,"11111"), msg="Course exists in the datbase should match result")

    def test_get_course_info_2(self):
        test_dic = {}
        self.assertEqual(test_dic, functions.Course.get_course_info("11112"), msg="Course does not exist result should be empty")

    def test_update_course_info_1(self):
        test_dic = {'course_id': '11111', 'course_name': 'Test Course', 'course_code':101,'instructor_id':1}
        update_dic = {'course_id':"11111",'instructor_id': 1}
        functions.Course.update_course_info(update_dic)
        self.assertEqual(test_dic, functions.Course.get_course_info("11111"),msg="Course should be updated with instructor")

    def test_update_course_info_2(self):
        test_dic = {'course_id': '11111', 'course_name': 'Test 2 Course'}
        self.assertEqual(False, functions.Course.update_course_info(test_dic),msg="Should return true because course exists")

    def test_update_course_info_3(self):
        test_dic = {'course_id': '11112', 'course_name': 'Test 2 Course'}
        self.assertEqual(False, functions.Course.update_course_info(test_dic),msg="Should return flase because course does not exists")

    def test_update_course_info_4(self):
        test_dic = {}
        self.assertEqual(False, functions.Course.update_course_info(test_dic),msg="Should return flase because dictionary is empty")

    def test_delete_course_1(self):
        functions.Course.delete_course(course_id="11111")
        self.assertEqual({},functions.Course.delete_course("11111"),msg="Should return nothing since course should have been deleted from database")

    def test_delete_course_2(self):
        self.assertEqual(False,functions.Course.delete_course("12345"),msg="Should return false since course does not exist")

"New commit"

class LabSectionTests(TestCase):
    ""

class TATests(TestCase):
    ""