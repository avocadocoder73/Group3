from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor, instructor, TA I would like to see all courses so that I can be informed on the classes being taught.
"""


class ViewCourses(TestCase):
    """Setup for ViewCourses acceptance test"""

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
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """Teardown for ViewCourses acceptance test"""

    def tearDown(self):
        self.temp3.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()
        self.test_lab_section.delete()

    """Testing seeing all the courses on the page"""

    def test_viewcourses(self):
        response = self.client.get('/view-courses/')

        # Check that we get a response
        self.assertEqual(response.status_code, 200)

        response_list = [response.context['courses'], response.context['course_sections'],
                         response.context['lab_sections']]
        test_list = [functions.Course_func.get_all(self), functions.CourseSection_func.get_all(self),
                     functions.LabSection_func.get_all(self)]

        # check the context for the lists for courses
        self.assertEqual(test_list, response_list,
                         msg="View Courses should have all the information when get request is given")
