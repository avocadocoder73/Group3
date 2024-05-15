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

    """test for failing to deleting a course section"""

    def test_delete_Course_Section2(self):
        functions.CourseSection_func.Delete(self, "456")
        self.assertEqual([], functions.CourseSection_func.get(self, query="section_id", identity='456'))