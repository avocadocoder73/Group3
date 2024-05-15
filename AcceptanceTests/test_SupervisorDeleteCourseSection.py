from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to delete course sections so that if a section is not going to be taught, I can remove it.
"""


class SupervisorDeleteCourseSectionTest(TestCase):
    """Setup for delete course tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="S")
        self.temp.save()
        self.temp_course = Course(course_id="CS101", course_name="Test Course", course_term="F")
        self.temp_course.save()
        self.test_courseSection = CourseSection(section_id=4560, section_number=202, course=self.temp_course,
                                                Time="MW 9:30AM", Location="EMS", credits=3, instructor=self.temp)
        self.test_courseSection.save()
        self.client = Client()
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """Teardown for delete course section tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()

    """Testing the valid course deletion"""

    def test_ValidDeleteCourseSection1(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "4560", "status": "delete_courseSection"}, follow=True)
        self.assertEqual(resp.context['message'], "Course Section Deletion successful",
                         msg="Message for successful course section creation failed")

    """Test the valid course deletion"""

    def test_ValidDeleteCourseSection2(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "4560", "status": "delete_courseSection"}, follow=True)
        self.assertEqual([], functions.CourseSection_func.get(self, "section_id", "4560"),
                         msg="Message for successful course section creation failed")

    """Test invalid course deletion"""

    def test_InvalidDeleteCourseSection1(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "45600", "status": "delete_courseSection"}, follow=True)
        self.assertEqual(resp.context['message'], "Course section does not exist",
                         msg="Message for successful course section creation failed")
