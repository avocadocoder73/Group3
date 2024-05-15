from django.test import TestCase, Client
from TA_APP.models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions

"""Test the LabSection_func class"""


class LabSectionTests(TestCase):
    """Setup for tests"""

    def setUp(self):
        self.temp2 = User(name="Test2", username="test_user2", password="PASSWORD2", email="test2@uwm.edu",
                          phone_number=1234567893, address="123 1st street", type="Instructor")
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567894, address="222 1st street", type="TA")
        self.temp_course = Course(course_id="CS303", course_name="Test Course", course_term="F")
        self.test_courseSection = CourseSection(section_id=123, section_number=303, course=self.temp_course,
                                                Time="MW 9:30AM", Location="EMS", credits=3, instructor=self.temp2)
        self.test_lab_section = LabSection(section_id=222, section_number=301, course_section=self.test_courseSection,
                                           course=self.temp_course, Time="MW 9:30AM", Location="EMS",
                                           Type="L", ta=self.temp3)
        self.test_lab_section1 = LabSection(section_id=11111, section_number=801,
                                            course_section=self.test_courseSection,
                                            course=self.temp_course, Time="MW 9:30AM", Location="EMS", Type="L",
                                            ta=self.temp3)
        self.test_lab_section2 = LabSection(section_id=11112, section_number=802,
                                            course_section=self.test_courseSection,
                                            course=self.temp_course, Time="MW 9:30AM", Location="EMS", Type="L",
                                            ta=self.temp3)
        self.temp2.save()
        self.temp3.save()
        self.temp_course.save()
        self.test_courseSection.save()
        self.test_lab_section.save()
        self.test_lab_section1.save()
        self.test_lab_section2.save()

    """Teardown for tests"""

    def tearDown(self):
        self.temp2.delete()
        self.temp3.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()
        self.test_lab_section.delete()
        self.test_lab_section1.delete()
        self.test_lab_section2.delete()

    """test for getting a lab section"""

    def test_get_labSection_info(self):
        test_dic = {"section_id": 222, "section_number": 301, "course_section": self.test_courseSection.section_id,
                    "course": self.temp_course.course_id, "Time": "MW 9:30AM", "Location": "EMS",
                    "Type": "L", "ta": self.temp3.name}
        test_list = [test_dic]
        self.assertEqual(test_list, functions.LabSection_func.get(self, query='section_id', identity='222'))

    """Test for failing to get a lab section"""

    def test_get_labSection_info_fail(self):
        self.assertEqual([], functions.LabSection_func.get(self, query='section_id', identity='999'))

    """test for getting all lab sections"""

    def test_getAll_labSection_info(self):
        test_dic = {"section_id": 222, "section_number": 301, "course_section": self.test_courseSection.section_id,
                    "course": self.temp_course.course_id, "Time": "MW 9:30AM", "Location": "EMS",
                    "Type": "L", "ta": self.temp3.name}
        test_dic1 = {'section_id': 11111, 'section_number': 801,
                     'course_section': self.test_courseSection.section_id,
                     'course': self.temp_course.course_id, 'Time': 'MW 9:30AM', 'Location': 'EMS',
                     'Type': 'L', 'ta': self.temp3.name}
        test_dic2 = {'section_id': 11112, 'section_number': 802,
                     'course_section': self.test_courseSection.section_id,
                     'course': self.temp_course.course_id, 'Time': 'MW 9:30AM', 'Location': 'EMS',
                     'Type': 'L', 'ta': self.temp3.name}
        expected_result = [test_dic, test_dic1, test_dic2]
        self.assertEqual(expected_result, functions.LabSection_func.get_all(self))

    """test for creating a lab section"""

    def test_create_labSection(self):
        info = {"section_id": 987, "section_number": 302, "course_section": self.test_courseSection.section_id,
                "course": self.temp_course.course_id, "Time": "MW 9:30AM", "Location": "EMS", "Type": "L",
                "ta": self.temp3.name}
        self.assertTrue(functions.LabSection_func.Create(self, info))

    """test for failing to create a lab section"""

    def test_create_labSection_fail(self):
        info = {"section_number": 302, "course_section": self.test_courseSection,
                "course": self.temp_course, "Time": "MW 9:30AM", "Location": "EMS", "Type": "L", "ta": self.temp3}
        self.assertEqual(False, functions.LabSection_func.Create(self, info),
                         msg="Cannot create lab section without section id")

    """test for failing to create a lab section"""

    def test_create_labSection_fail2(self):
        info = {"section_id": 987, "section_number": 302, "course_section": self.test_courseSection,
                "Time": "MW 9:30AM", "Location": "EMS", "Type": "L", "ta": self.temp3}
        self.assertEqual(False, functions.LabSection_func.Create(self, info),
                         msg="Cannot create lab section without assigning course")

    """Test for failing to create a lab section"""

    def test_create_labSection_fail3(self):
        info = {"section_id": 222, "section_number": 301, "course_section": self.test_courseSection,
                "course": self.temp_course, "Time": "MW 9:30AM", "Location": "EMS", "Type": "L", "ta": self.temp3}
        self.assertEqual(False, functions.LabSection_func.Create(self, info),
                         msg="Cannot create lab section that is already there")

    """test for failing to create a lab section"""

    def test_create_labSection_fail4(self):
        info = {}
        self.assertEqual(False, functions.LabSection_func.Create(self, info),
                         msg="Cannot create lab section with an empty dictionary")

    """test for editing a lab section"""

    def test_edit_labSection(self):
        update_info = {"section_id": 222, "section_number": 401}
        updated_info = {"section_id": 222, "section_number": 401,
                        "course_section": self.test_courseSection.section_id,
                        "course": self.temp_course.course_id, "Time": "MW 9:30AM", "Location": "EMS",
                        "Type": "L", "ta": self.temp3.name}
        updated_info_list = [updated_info]
        self.assertTrue(functions.LabSection_func.Edit(self, update_info))
        self.assertEqual(updated_info_list, functions.LabSection_func.get(self, query='section_id', identity='222'))

    """test for failing editing a lab section"""

    def test_edit_labSection_invalid_section_id(self):
        update_info = {"section_id": 999, "section_number": 401}
        self.assertFalse(functions.LabSection_func.Edit(self, update_info))

    """test for deleting a lab section"""

    def test_delete_labSection_invalid_section_id(self):
        identity = "999"
        self.assertFalse(functions.LabSection_func.Delete(self, identity))

    """test for failing deleting a lab section"""

    def test_delete_labSection(self):
        identity = "222"
        self.assertTrue(functions.LabSection_func.Delete(self, identity))
