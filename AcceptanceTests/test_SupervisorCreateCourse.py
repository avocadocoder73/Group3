from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to create courses for staff so that I can designate them to their respective class to teach
"""


class SupervisorCreateCourseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_createCourse(self):
        response = self.client.post('/course-management/',
                                    {"courseid": "1", "name": "Chemistry 101", "term": "F", "createcourse": "true"})

        course = Course.objects.get(course_name="Chemistry 101")

        self.assertEqual(course.course_term, "F")

        course.delete()

    def test_invalidCoursecreation(self):
        response = self.client.post('/course-management/', {"course_name": "", "createcourse": "true"})

        self.assertEqual(response.context['create_course'], "Course Creation Failed")
