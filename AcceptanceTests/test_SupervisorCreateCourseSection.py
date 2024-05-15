from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to create Course sections so that the courses in the system have lecture sections.
"""


class SupervisorCreateCourseSectionTest(TestCase):
    """Setup for the creation of Course sections"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="S")
        self.instructor = User(name="Test2", username="test_user2", password="PASSWORD", email="test2@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="I")
        self.temp.save()
        self.instructor.save()
        self.temp_course = Course(course_id="CS101", course_name="Test Course", course_term="F")
        self.temp_course.save()
        self.test_courseSection = CourseSection(section_id=4560, section_number=202, course=self.temp_course,
                                                Time="MW 9:30AM", Location="EMS", credits=3, instructor=self.temp)
        self.test_courseSection.save()
        self.client = Client()
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """Teardown for the creation of Course sections"""

    def tearDown(self):
        self.temp.delete()
        self.instructor.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()

    """Testing the valid creation of a course section"""

    def test_ValidCreateCourseSection1(self):
        resp = self.client.post('/course-management/',
                                {"sectionid": "456", "sectionnumber": "201", "course": "CS101",
                                 "time": "MW 9:30AM", "location": "EMS", "credits": "3", "instructor":self.instructor.name,
                                 "createcoursesection": "true"}, follow=True)
        self.assertEqual(resp.context['create_course_section_message'], "Course Section Created Successfully",
                         msg="Message for successful course section creation failed")

    """Testing the valid creation of a course section"""

    def test_ValidCreateCourseSection2(self):
        resp = self.client.post('/course-management/',
                                {"sectionid": "456", "sectionnumber": "201", "course": "CS101",
                                 "time": "MW 9:30AM", "location": "EMS", "credits": "3", "instructor":self.instructor.name,
                                 "createcoursesection": "true"}, follow=True)
        self.assertEqual(201, CourseSection.objects.get(section_number=201).section_number,
                         msg="Message for successful course section creation failed")

    """Testing the invalid creation of a course section"""

    def test_InvalidCreateCourseSection1(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "456", "section_number": '', "course": "CS101",
                                 "Time": "MW 9:30AM", "Location": "EMS", "credits": "3",
                                 "createcoursesection": "true"}, follow=True)
        self.assertEqual(resp.context['create_course_section_message'], "Course Section Creation Failed",
                         msg="Message for unsuccessful course section creation failed")

    """Testing the invalid creation of a course section"""

    def test_InvalidCreateCourseSection2(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "456", "section_number": "202", "course": "CS101",
                                 "Time": "MW 9:30AM", "Location": "EMS", "credits": "3",
                                  "createcoursesection": "true"}, follow=True)
        self.assertEqual(resp.context['create_course_section_message'], "Course Section Creation Failed",
                         msg="Message for unsuccessful course section creation failed")

