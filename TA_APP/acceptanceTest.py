import unittest
from TA_Scheduling.wsgi import *
from django.test import TestCase, Client
from TA_APP.models import User, Course, CourseSection, LabSection
from django.core.exceptions import ObjectDoesNotExist
import TA_APP.functions as functions

"""
PBI: As a user I would like to be able to sign into my account so that I can access it securely
"""
class LoginTest(TestCase):
    """The setpUp for LoginTests"""
    def setUp(self):
        self.user = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="S")
        self.user.save()
        self.client = Client()

    """Teardown for login tests"""
    def tearDown(self):
        self.user.delete()

    """Testing the valid login information"""
    def test_validLogin(self):
        response = self.client.post("/", {"username": "test_user", "password": "PASSWORD"})
        ##routes to homepage if valid

        self.assertEqual(response.context['status'], "Signed In")


    """Testing the login with invalid username and password"""
    def test_invalidLogin(self):
        response = self.client.post("/", {"username": "test_user42", "password": "PASSWORD123"})



        ##if html contains message that username or password is incorrect creds are invalid
        self.assertEqual(response.context['message'], 'Username or password is incorrect')



"""
PBI: As a supervisor I would like to create accounts for staff so that I can assign their responsibilities
"""

class SupervisorCreateAccountTest(TestCase):
    """Setup for creating accounts tests"""
    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="S")
        self.temp.save()
        self.client = Client()
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """The teardown for creating accounts tests"""

    def tearDown(self):
        self.temp.delete()
        try:
            user = User.objects.get(username="test_user4")
            if user is not None:
                user.delete()
        except Exception as e:
            print(e)



    """Testing the valid creation of an account"""
    def test_ValidCreateAccount1(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test4', 'username': 'test_user4', 'password': 'PASSWORD4',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)

        self.assertEqual(resp.context['message'], "Account Created Successfully",
                         msg="Message for successful account creation failed")

    """Testing the valid creation of an account"""
    def test_ValidCreateAccount2(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test4', 'username': 'test_user4', 'password': 'PASSWORD4',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)
        self.assertEqual("test_user4", User.objects.get(username="test_user4").username,
                         msg="Account should be present in the database.")

    """Testing the invalid creation of an account"""
    def test_InvalidCreateAccount1(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD4',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)

        self.assertEqual(resp.context['message'], "Duplicate username or missing form field",
                         msg="Message for duplicate account creation failed")

    """Testing the invalid creation of an account"""
    def test_InvalidCreateAccount2(self):
        resp = self.client.post('/account-management/',
                                {'name': 'Test', 'password': 'test_user',
                                 'email': 'test@uwm.edu', 'phone': "1234567890", 'address': '123 1st Street',
                                 "role": "TA", 'skills': '', 'status': 'create'}, follow=True)

        self.assertEqual(resp.context['message'], "Duplicate username or missing form field",
                         msg="Message for missing field account creation failed")


"""
PBI: As a supervisor I would like to delete accounts for staff so that I can delete accounts of individuals who do not work at the school anymore
"""

class SupervisorDeleteAccountTest(TestCase):
    """Testing the setup for deleting a account"""
    def setUp(self):
        self.user = User(username="newestuser", password="newestuser2")
        self.user.save()
        self.client = Client()

    """Test deleting an account"""
    def test_deleteaccount(self):
        response = self.client.post('/account-management/',
                                    {"delusername": "newestuser", "password": "newestuser2", "status": "delete"})

        with self.assertRaises(ObjectDoesNotExist):
                User.objects.get(username="newestuser")

    """Test deleting an invalid account"""
    def test_invaliddeletion(self):
        response = self.client.post('/account-management/', {"delusername": "newestuser10", "password": "42", "status": "delete"})

        self.assertEqual(response.context['message'], "Account Deletion Failed")


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

"""
PBI: As a supervisor I would like to delete course sections so that if a section is not going to be taught, I can remove it.
"""
class SupervisorDeleteCourseSectionTest(TestCase):
    """Setup for delete course tests"""
    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="S")
        self.temp.save()
        self.temp_course = Course(course_id="CS101", course_name="Test Course", course_term="F")
        self.temp_course.save()
        self.test_courseSection = CourseSection(section_id=4560, section_number=202, course=self.temp_course,
                                                Time="MW 9:30AM", Location="EMS", credits=3, instructor=self.temp)
        self.test_courseSection.save()
        self.client = Client()
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

    """Teardown for delete course section tests"""
    def tearDown(self):
        self.temp.delete()
        self.temp_course.delete()
        self.test_courseSection.delete()

    """Testing the valid course deletion"""
    def test_ValidDeleteCourseSection1(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "4560", "status": "delete_courseSection"}, follow=True)
        self.assertEqual(resp.context['message'], "Course Section Deletion successful",
                         msg="Message for successful course section creation failed")

    """Test the valid course deletion"""
    def test_ValidDeleteCourseSection2(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "4560", "status": "delete_courseSection"}, follow=True)
        self.assertEqual([], functions.CourseSection_func.get(self, "section_id", "4560"),
                         msg="Message for successful course section creation failed")

    """Test invalid course deletion"""
    def test_InvalidDeleteCourseSection1(self):
        resp = self.client.post('/course-management/',
                                {"section_id": "45600", "status": "delete_courseSection"}, follow=True)
        self.assertEqual(resp.context['message'], "Course section does not exist",
                         msg="Message for successful course section creation failed")

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

"""
PBI: As a supervisor I would like to see all users and all their personal information so that I can have detailed records of staff.
PBI: As a Instructor, TA I would like to see all users so that I can see all of the staff in my department.
"""
class ViewUsers(TestCase):
    """setup for viewusers tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="I")
        self.temp.save()
        self.temp2 = User(name="Test2", username="test_user2", password="PASSWORD2", email="test@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="TA")
        self.temp2.save()
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="S")
        self.temp3.save()
        self.client = Client()

    """Teardown for view users info tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp2.delete()
        self.temp3.delete()

    """Test viewing all the users on the page"""

    def test_viewusers(self):
        """Set session"""
        session = self.client.session
        session['username'] = 'test_user3'
        session.save()

        response = self.client.get('/view-users/')



        # Check that we get a response
        self.assertEqual(response.status_code, 200)

        # check the context for the lists for courses
        self.assertEqual(functions.User_func.get_all(self), response.context['users'],
                         msg="View Courses should have all the information when get request is given")

"""
PBI: As a Supervisor, Instructor, TA I want to edit my own contact information, so that students and staff my reach me.
"""
class EditContactInformation(TestCase):
    """Setup for edit contact info tests"""

    def setUp(self):
        self.temp = User(name="Test", username="test_user", password="PASSWORD", email="test@uwm.edu",
                         phone_number=1234567890, address="123 1st street", type="I")
        self.temp.save()
        self.temp2 = User(name="Test2", username="test_user2", password="PASSWORD2", email="test@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="TA")
        self.temp2.save()
        self.temp3 = User(name="Test3", username="test_user3", password="PASSWORD3", email="test3@uwm.edu",
                          phone_number=1234567890, address="123 1st Street", type="S")
        self.temp3.save()
        self.client = Client()

    """Teardown for edit contact info tests"""

    def tearDown(self):
        self.temp.delete()
        self.temp2.delete()
        self.temp3.delete()

    """Testing if a supervisor can edit their own contact info"""

    def test_edit_contact_supervisor(self):
        session = self.client.session
        session['username'] = 'test_user3'
        session.save()

        new_list = [{'name': 'Test3', 'username': 'test_user3', 'password': 'PASSWORD3',
                     'email': 'test3@uwm.edu', 'phone_number': 4567892122, 'address': '123 1st Street', "type": "S",'skills': ''}]

        response = self.client.post('/editcontactinfo/',
                                    {
                                     'email': 'test3@uwm.edu', 'phone': "4567892122",
                                     'address': '123 1st Street', "status": "edit_contact"},
                                    follow=True)


        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user3"))

    """Testing if a supervisor can edit their own contact info"""

    def test_edit_contact_instructor(self):
        session = self.client.session
        session['username'] = 'test_user'
        session.save()

        new_list = [{'name': 'Test', 'username': 'test_user', 'password': 'PASSWORD',
                     'email': 'test6@uwm.edu', 'phone_number': 4327537522, 'address': '123 3rd Street', "type": "I",
                     'skills': ''}]

        response = self.client.post('/editcontactinfo/',
                                    {'email': 'test6@uwm.edu', 'phone': "4327537522",
                                     'address': '123 3rd Street'},
                                    follow=True)

        print(functions.User_func.get(self, query="username", identity="test_user"))

        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user"))

    """Testing if a TA can edit their own contact info including their skills information"""

    def test_edit_contact_TA(self):
        session = self.client.session
        session['username'] = 'test_user2'
        session.save()

        new_list = [{'name': 'Test2', 'username': 'test_user2', 'password': 'PASSWORD2',
                     'email': 'test5@uwm.edu', 'phone_number': 3123543444, 'address': '123 1st Street', "type": "TA",
                     'skills': ''}]

        response = self.client.post('/editcontactinfo/',
                                    {
                                     'email': 'test5@uwm.edu', 'phone': "3123543444",
                                     'address': '123 1st Street'},
                                    follow=True)



        self.assertEqual(new_list, functions.User_func.get(self, query="username", identity="test_user2"))


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

        self.assertEqual("test_user",self.test_courseSection.instructor.username,msg="Instructor should be assigned to section now")

    """Test a instructor adding a TA to a lab section"""
    def test_addTAToLab(self):
        response = self.client.post("/placeholder", {"username": "test_user2", "lab_section": "302"}, follow=True)

        self.assertEqual("test_user2", self.test_lab_section.ta.username,
                         msg="TA should be assigned to lab section now")
