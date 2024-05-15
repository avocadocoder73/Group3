from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions

"""
PBI: As a supervisor I would like to delete courses so that I can remove the courses that are no longer taught
"""


class SupervisorDeleteCourseTest(TestCase):
    """Setup the deleting a course tests"""

    def setUp(self):
        self.Course = Course(course_name="Chemistry 101")
        self.Course.save()
        self.client = Client()

    """The testing of a valid course deletion"""

    def test_validCourseDeletion(self):
        response = self.client.post('/homepage/', {"course_name": "Chemistry 101", "status": "delete_course"})

        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(course_name="newestuser")

    """Testing of invalid course deletion"""
    def test_invalidCourseDeletion(self):
        response = self.client.post('/homepage/', {"course_name": "SuperFunClass 101", "status": "delete_course"})

        self.assertEqual(response.content, "Course does not exist to be deleted")
        self.Course.delete()
