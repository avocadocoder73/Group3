from django.test import TestCase, Client
from TA_APP.models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions

"""Test Course_func class"""


class CourseTests(TestCase):
    """Setup for Course_func tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="TA")
        self.temp.save()
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567890, address="123 1st street", type="I")
        self.temp3.save()
        self.temp_course = Course(course_id="CS101", course_name="Test Course", course_term="F")
        self.temp_course.save()
        self.temp2_course = Course(course_id="CS102", course_name="Test Course 2", course_term="F")
        self.temp2_course.save()
        self.section = CourseSection(section_id="11111", section_number=801,
                                     course=self.temp_course, Time="MW 9:30AM", Location="EMS", credits=3,
                                     instructor=self.temp3)
        self.section.save()
        self.section2 = CourseSection(section_id="11112", section_number=801,
                                      course=self.temp2_course, Time="MW 9:30AM", Location="EMS", credits=3,
                                      instructor=self.temp3)
        self.section2.save()

    """teardown for Course_func tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp3.delete()
        self.temp_course.delete()
        self.temp2_course.delete()
        self.section.delete()
        self.section2.delete()

    """Tests for getting course based on course_id"""

    def test_get_course_info_1(self):
        test_dic = {'course_id': 'CS101', "course_name": "Test Course", "course_term": "Fall"}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.Course_func.get(self, query="course_id", identity="CS101"),
                         msg="Course exists in the database should match result")

    """Tests for getting course based on course_name"""

    def test_get_course_info_2(self):
        test_dic = {'course_id': 'CS101', "course_name": "Test Course", "course_term": "Fall"}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.Course_func.get(self, query="course_name", identity="Test Course"),
                         msg="Course exists in the database should match result")

    """Tests for getting course based on course_term"""

    def test_get_course_info_3(self):
        test_dic = {'course_id': 'CS101', "course_name": "Test Course", "course_term": "Fall"}
        test_dic2 = {'course_id': 'CS102', "course_name": "Test Course 2", "course_term": "Fall"}
        test_list = [test_dic, test_dic2]
        self.assertEqual(test_list, functions.Course_func.get(self, query="course_term", identity="Fall"),
                         msg="Course exists in the database should match result")

    """Tests for getting course that does not exist"""

    def test_get_course_info_4(self):
        test_list = []
        self.assertEqual(test_list, functions.Course_func.get(self, query="course_id", identity="CS1000"),
                         msg="Course does not exist result should be empty")

    """Tests for getting all courses in the database"""

    def test_get_all_courses(self):
        test_dic = {'course_id': 'CS101', "course_name": "Test Course", "course_term": "Fall"}
        test_dic2 = {'course_id': 'CS102', "course_name": "Test Course 2", "course_term": "Fall"}
        test_list = [test_dic, test_dic2]
        self.assertEqual(test_list, functions.Course_func.get_all(self), msg="Courses not showing up properly")



    """Test for creating a valid course"""

    def test_create_course_1(self):
        test_dic = {'course_id': 'CS201', "course_name": "Test Course 201", "course_term": "Fall"}
        self.assertEqual(True, functions.Course_func.Create(self, info=test_dic),
                         msg="Operation should have been successful")
        temp_user = Course.objects.get(course_id="CS201")
        temp_user.delete()

    """Test for creating an invalid course"""

    def test_create_course_2(self):
        test_dic = {'course_id': 'CS201', "course_term": "Fall"}
        self.assertEqual(False, functions.Course_func.Create(self, info=test_dic),
                         msg="Incorrect dictionary operation is should be unsuccessful")

    """Test for creating a course but using a invalid dictionary"""

    def test_create_course_3(self):
        test_dic = {}
        self.assertEqual(False, functions.Course_func.Create(self, info=test_dic),
                         msg="Empty dictionary operation is unsuccessful")

    """Test for creating a repeated course"""

    def test_create_course_4(self):
        test_dic = {'course_id': 'CS101', "course_name": "Test Course 201", "course_term": "Fall"}
        self.assertEqual(False, functions.Course_func.Create(self, info=test_dic),
                         msg="Operation should not have been successful because you cannot repeat course ID")


    """Test for editing an existing course"""

    def test_edit_course_info_1(self):
        test_dic = {'course_id': 'CS101', "course_term": "Spring"}
        self.assertEqual(True, functions.Course_func.Edit(self, test_dic),
                         msg="Should return true because course exists")

    """Test for editing an non-existing course"""

    def test_edit_course_info_2(self):
        test_dic = {'course_id': 'CS1010', "course_term": "Spring"}
        self.assertEqual(False, functions.Course_func.Edit(self, test_dic),
                         msg="Should return false because course does not exists")

    """Test for editing an non-existing course"""

    def test_edit_course_info_3(self):
        test_dic = {'course_id': 'CS1010', "course_term": "Spring"}
        self.assertEqual(False, functions.Course_func.Edit(self, test_dic),
                         msg="Should return false because course does not exists")

    """Test for editng a course without an input dictionary"""

    def test_edit_course_info_4(self):
        test_dic = {}
        self.assertEqual(False, functions.Course_func.Edit(self, test_dic),
                         msg="Should return false because dictionary is empty")

    """Tests for deleting an existing course"""

    def test_delete_course_1(self):
        self.assertEqual(True, functions.Course_func.Delete(self, identity='CS101'),
                         "User should successfully delete")

    """Tests for deleting a non-existing course"""

    def test_delete_course_2(self):
        self.assertEqual(False, functions.Course_func.Delete(self, identity='CS2000'),
                         "User should not exist in the database")


