from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to delete lab sections so that if a section is not going to be taught, I can remove it.
"""


class SupervisorDeleteLabSectionTest(TestCase):
    """The setup for deleting a lab section"""

    def setUp(self):
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567894, address="222 1st street", type="TA")
        self.temp_course = Course(course_id="CS303", course_name="Test Course", course_term="F")
        self.test_courseSection = CourseSection(section_id=123, section_number=303, course=self.temp_course,
                                                Time="MW 9:30AM", Location="EMS", credits=3, instructor=self.temp3)
        self.test_lab_section = LabSection(section_id=222, section_number=302,
                                           course_section=self.test_courseSection,
                                           course=self.temp_course, Time="MW 9:30AM", Location="EMS",
                                           Type="L", ta=self.temp3)
        self.temp3.save()
        self.temp_course.save()
        self.test_courseSection.save()
        self.test_lab_section.save()
        self.client = Client()
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """Teardown for deleting a lab section"""

    def tearDown(self):
        self.temp3.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()
        self.test_lab_section.delete()

    """Testing a valid deletion of a lab section"""

    def test_ValidDeleteLabSection1(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "222", "status": "delete_labSection"}, follow=True)
        self.assertEqual(resp.context['message'], "Lab Section Deletion successful",
                         msg="Message for successful course section creation failed")

    """Testing a valid deletion of a lab section"""

    def test_ValidDeleteLabSection2(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "222", "status": "delete_labSection"}, follow=True)
        self.assertEqual([], functions.LabSection_func.get(self, "section_id", "222"),
                         msg="Message for successful course section creation failed")

    """Testing a invalid deletion of a lab section"""

    def test_InvalidDeleteLabSection1(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "45600", "status": "delete_labSection"}, follow=True)
        self.assertEqual(resp.context['message'], "Course section does not exist",
                         msg="Message for successful course section creation failed")
