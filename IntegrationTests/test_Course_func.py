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

    """test for creating a valid course"""

    def test_create_course_1(self):
        test_dic = {'course_id': 'CS201', "course_name": "Test Course 201", "course_term": "Fall"}
        test_list = [test_dic]
        functions.Course_func.Create(self, info=test_dic)
        self.assertEqual(test_list, functions.Course_func.get(self, query='course_id', identity='CS201'),
                         msg="Course not found")
        temp_user = Course.objects.get(course_id="CS201")
        temp_user.delete()

    """Test for editing a valid course"""

    def test_edit_course_info_1(self):
        test_dic = {'course_id': 'CS101', "course_term": "Spring"}
        updated_dic = {'course_id': 'CS101', "course_name": "Test Course", "course_term": "Spring"}
        updated_list = [updated_dic]
        functions.Course_func.Edit(self, info=test_dic)
        self.assertEqual(updated_list, functions.Course_func.get(self, query="course_id", identity="CS101"),
                         msg="Course should be updated with new term")

    """Test for editing an existing course"""

    def test_edit_course_info_2(self):
        test_dic = {'course_id': 'CS101', "course_name": "Test course 200", "course_term": "Spring"}
        updated_dic = {'course_id': 'CS101', "course_name": "Test course 200", "course_term": "Spring"}
        updated_list = [updated_dic]
        functions.Course_func.Edit(self, info=test_dic)
        self.assertEqual(updated_list, functions.Course_func.get(self, query="course_id", identity="CS101"),
                         msg="Course should be updated with new term")

    """Tests for deleting a existing course"""

    def test_delete_course_1(self):
        functions.Course_func.Delete(self, identity='CS101')
        self.assertEqual([], functions.Course_func.get(self, query="course_id", identity='CS101'),
                         "User should not exist in the database")