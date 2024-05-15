from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to create lab sections so that the courses in the system have lab sections.
"""


class SupervisorCreateLabSectionTest(TestCase):
    """Setup for lab sections tests creation"""

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

    """Teardown for lab section creation tests"""

    def tearDown(self):
        self.temp3.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()
        self.test_lab_section.delete()

    """Test valid lab section creation"""

    def test_ValidCreateLabSection1(self):
        resp = self.client.post('/course-management/',
                                {"sectionid": "223", "sectionnumber": "301",
                                 "coursesection": "123",
                                 "course": "CS303", "time": "MW 9:30AM", "location": "EMS",
                                 "role": "L", "ta":"Test3", "createlabsection": "true"}, follow=True)
        self.assertEqual(resp.context['lab_message'], "Lab Section Created Successfully",
                         msg="Message for successful course section creation failed")

    """test valid lab section creation"""

    def test_ValidCreateLabSection2(self):
        resp = self.client.post('/course-management/',
                                {"sectionid": "223", "sectionnumber": "301",
                                 "coursesection": "123",
                                 "course": "CS303", "time": "MW 9:30AM", "location": "EMS",
                                 "role": "L","ta":"Test3",  "createlabsection": "true"}, follow=True)
        self.assertEqual(301, LabSection.objects.get(section_number=301).section_number,
                         msg="Message for successful course section creation failed")

    """Test invalid lab section creation"""

    def test_InvalidCreateLabSection1(self):
        resp = self.client.post('/course-management/',
                                {"sectionid": "223", "sectionnumber": "301",
                                 "coursesection": '',
                                 "course": "CS303", "time": "MW 9:30AM", "location": "EMS",
                                 "role": "L", "ta":"Test3",  "createlabsection": "true"}, follow=True)
        self.assertEqual(resp.context['lab_message'], "Lab Section Creation Failed",
                         msg="Message for unsuccessful course section creation failed because of duplicate")

    """Test the invalid creation of a lab section"""

    def test_InvalidCreateLabSection2(self):
        resp = self.client.post('/course-management/',
                                {"sectionid": "222", "sectionnumber": "302",
                                 "coursesection": "303",
                                 "course": "CS303", "time": "MW 9:30AM", "location": "EMS",
                                 "role": "L", "ta":"Test3", "createlabsection": "true"}, follow=True)
        self.assertEqual(resp.context['lab_message'], "Lab Section Creation Failed",
                         msg="Message for unsuccessful course section creation failed")
