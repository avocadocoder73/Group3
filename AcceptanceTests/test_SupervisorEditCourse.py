from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions


"""
PBI: As a supervisor I would like to edit courses and sections so that I can update the courses that have changed.
"""


class SupervisorEditCourseTest(TestCase):
    """Setup for editing a course"""

    def setUp(self):
        self.Course = Course(course_name="Chemistry 101")
        self.Course.save()
        self.client = Client()

    """Teardown for editing a course"""

    def tearDown(self):
        self.Course.delete()

    """Testing a valid editing of a course"""

    def validCourseEdit(self):
        response = self.client.post('/homepage/',
                                    {"course_name": "Chemistry 101", "editdata": {"course_name": "Chemistry 102"},
                                     "status": "edit_course"})

        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(course_name="Chemistry 101")

    """Testing a invalid editing of a course"""

    def invalidCourseEdit(self):
        response = self.client.post('/homepage/',
                                    {"course_name": "Chemistry 102", "editdata": {"course_name": "Chemistry 103"},
                                     "status": "edit_course"})

        self.assertEqual(response.content, "Course does not exist to be edited")

