from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to assign users to courses so that the proper faculty and registered students are enrolled
"""


class SupervisorAssignUserToCourseTest(TestCase):
    """Setup for SupervisorAssignUsertoCourse acceptance test"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="I")
        self.temp.save()
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
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """Teardown for SupervisorAssignUsertoCourse acceptance test"""

    def tearDown(self):
        self.temp3.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()
        self.test_lab_section.delete()

    """Test adding an instructor"""

    def test_AssignUserToCourse1(self):
        response = self.client.post("/placeholder", {"username": "test_user", "course": "CS303"}, follow=True)

        self.assertEqual(True, (self.temp in self.temp_course.assignments.all()),
                         msg="Instructor should be in the manytomany of CS303")

    """Test adding a TA"""

    def test_AssignUserToCourse2(self):
        response = self.client.post("/placeholder", {"username": "test_user3", "course": "CS303"}, follow=True)

        self.assertEqual(True, (self.temp3 in self.temp_course.assignments.all()),
                         msg="TA should be in the manytomany of CS303")
