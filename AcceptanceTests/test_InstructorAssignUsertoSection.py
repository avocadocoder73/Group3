from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As an Instructor I would like to assign myself and TAs to course and lab sections so that I can make sure every course I am assigned to me am teaching a section and I have TAs for the labs.
"""


class InstructorAssignUserToSection(TestCase):
    """Setup for assigning to section"""

    def setUp(self):
        """Setup users and courses"""
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="I")
        self.temp.save()
        self.temp2 = User(name="Test2", username="test_user2", password="PASSWORD2", email="test@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="TA")
        self.temp2.save()
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="S")
        self.temp3.save()
        self.temp_course = Course(course_id="CS303", course_name="Test Course", course_term="F")
        self.test_courseSection = CourseSection(section_id=123, section_number=303, course=self.temp_course,
                                                Time="MW 9:30AM", Location="EMS", credits=3, instructor=self.temp3)
        self.test_lab_section = LabSection(section_id=222, section_number=302,
                                           course_section=self.test_courseSection,
                                           course=self.temp_course, Time="MW 9:30AM", Location="EMS",
                                           Type="L", ta=self.temp3)
        self.temp_course.save()
        self.test_courseSection.save()
        self.test_lab_section.save()
        """Add them to course"""
        self.temp_course.assignments.add(self.temp)
        self.temp_course.assignments.add(self.temp2)
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """teardown for tests"""

    def teardown(self):
        self.temp.delete()
        self.temp2.delete()
        self.temp3.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()
        self.test_lab_section.delete()

    """Test a instructor adding themselves to a course"""

    def test_addInstructorToSection(self):
        response = self.client.post("/placeholder", {"username": "test_user", "course_section": "303"}, follow=True)

        self.assertEqual("test_user", self.test_courseSection.instructor.username,
                         msg="Instructor should be assigned to section now")

    """Test a instructor adding a TA to a lab section"""

    def test_addTAToLab(self):
        response = self.client.post("/placeholder", {"username": "test_user2", "lab_section": "302"}, follow=True)

        self.assertEqual("test_user2", self.test_lab_section.ta.username,
                         msg="TA should be assigned to lab section now")
