from django.test import TestCase, Client
from TA_APP.models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions

"""Test the CourseSection_func class"""


class CourseSectionTests(TestCase):
    """Setup for tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="Instructor")
        self.temp_course = Course(course_id="CS202", course_name="Test Course", course_term="F")
        self.test_courseSection = CourseSection(section_id=456, section_number=201, course=self.temp_course,
                                                Time="MW 9:30AM", Location="EMS", credits=3, instructor=self.temp)
        self.test_courseSection1 = CourseSection(section_id=567, section_number=501, course=self.temp_course,
                                                 Time="TTH 9:30AM", Location="EMS", credits=3, instructor=self.temp)
        self.temp.save()
        self.temp_course.save()
        self.test_courseSection.save()
        self.test_courseSection1.save()

    """Teardown for tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()
        self.test_courseSection1.delete()

    """Test getting a course section"""

    def test_get_Course_Section_info(self):
        test_dic = {"section_id": 456, "section_number": 201, "course": self.temp_course.course_id, "Time": "MW 9:30AM",
                    "Location": "EMS", "credits": 3, "instructor": self.temp.name}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.CourseSection_func.get(self, query='section_id', identity='456'))

    """Test failing to get a course section"""

    def test_get_Course_Section_info_fail(self):
        self.assertEqual([], functions.CourseSection_func.get(self, query='section_id', identity='999'))

    """Test for getting all the course sections"""

    def test_getAll_Course_Section_info(self):
        test_dic = {"section_id": 456, "section_number": 201, "course": self.temp_course.course_id,
                    "Time": "MW 9:30AM", "Location": "EMS", "credits": 3, "instructor": self.temp.name}
        test_dic1 = {"section_id": 567, "section_number": 501, "course": self.temp_course.course_id,
                     "Time": "TTH 9:30AM", "Location": "EMS", "credits": 3, "instructor": self.temp.name}
        expected_list = [test_dic, test_dic1]
        self.assertEqual(expected_list, functions.CourseSection_func.get_all(self))

    """Test for creating a course section"""

    def test_create_Course_Section(self):
        info = {"section_id": 345, "section_number": 300, "course": self.temp_course.course_id, "Time": "MW 5:30PM",
                "Location": "EMS", "credits": 3, "instructor": self.temp.name}
        self.assertTrue(functions.CourseSection_func.Create(self, info))

    """Test for failing to create a course section"""

    def test_create_Course_Section_fail(self):
        info = {"section_number": 201, "course": self.temp_course, "Time": "MW 9:30AM",
                "Location": "EMS", "credits": 3, "instructor": "Test3"}
        self.assertEqual(False, functions.CourseSection_func.Create(self, info),
                         msg="Cannot create course section without section id")

    """Test for failing to create a course section"""

    def test_create_Course_Section_fail2(self):
        info = {"section_id": "22222", "section_number": 801, "Time": "MW 9:30AM",
                "Location": "EMS", "credits": 3, "instructor": "Test3"}
        self.assertEqual(False, functions.CourseSection_func.Create(self, info),
                         msg="Cannot create course section without assigning course")

    """Test for failing to create a course section"""

    def test_create_Course_Section_fail3(self):
        info = {"section_id": 456, "section_number": 201, "course": self.temp_course, "Time": "MW 9:30AM",
                "Location": "EMS", "credits": 3, "instructor": self.temp}
        self.assertEqual(False, functions.CourseSection_func.Create(self, info),
                         msg="Cannot create course section that is already there")

    """Test for failing to create a course section"""

    def test_create_Course_Section_fail4(self):
        info = {}
        self.assertEqual(False, functions.CourseSection_func.Create(self, info),
                         msg="Cannot create course section with an empty dictionary")

    """Test for editing an existing course section"""

    def test_edit_Course_Section(self):
        update_info = {"section_id": 456, "Location": "Lubar Hall"}
        updated_info = {"section_id": 456, "section_number": 201, "course": self.temp_course.course_id,
                        "Time": "MW 9:30AM", "Location": "Lubar Hall", "credits": 3, "instructor": self.temp.name}
        updated_info_list = [updated_info]
        print("expected", updated_info_list)
        self.assertTrue(functions.CourseSection_func.Edit(self, update_info))
        print("result  ", functions.CourseSection_func.get(self, query='section_id', identity='456'))
        self.assertEqual(updated_info_list, functions.CourseSection_func.get(self, query='section_id', identity='456'))

    """Test for failing editing an non-existing course section"""

    def test_edit_course_section_invalid_section_id(self):
        update_info = {"section_id": 999, "Location": "Lubar Hall"}
        self.assertFalse(functions.CourseSection_func.Edit(self, update_info))

    """Test for deleting a course section"""

    def test_delete_Course_Section(self):
        identity = "456"
        self.assertTrue(functions.CourseSection_func.Delete(self, identity))

    """Test for failing to delete a course section"""

    def test_delete_Course_Section_fail(self):
        identity = "000"
        self.assertFalse(functions.CourseSection_func.Delete(self, identity))


