from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from .models import User, Course, LabSection, CourseSection
import TA_APP.functions as functions


class Login(View):
    def get(self, request):
        # Displays the login page.
        return render(request, 'login.html', {})

    def post(self, request):
        # Handles login form submission.
        username = request.POST['username']
        password = request.POST['password']
        # check identity
        verify = functions.Login.authenticate(self, str(username), str(password))

        # Redirects to the appropriate dashboard based on user type.
        if verify == 'S':  # Supervisor (or Administrator)
            request.session['username'] = username
            return render(request, 'homepage.html', {"status": "Signed In"})
        elif verify == 'I':  # Instructor
            request.session['username'] = username
            return redirect('instructor_dashboard')
        elif verify == 'T':  # TA
            request.session['username'] = username
            return redirect('ta_dashboard')
        else:
            # Redirects back to login page if authentication fails.
            return render(request, "login.html", {"message": "Username or password is incorrect"})


class HomePage(View):
    def get(self, request):
        # Redirects to login if session is not active.
        if not request.session.get('username'):
            return redirect('/')

    def post(self, request):
        # Handles logout.
        logout(request)
        return redirect('/')


class AccountManagement(View):
    def get(self, request):
        # Displays the account management page if user is a supervisor.
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            return render(request, 'accountmanagement.html')
        else:
            # Logs out if user is not authorized.
            logout(request)
            return redirect('/')

    def post(self, request):
        # Handles account management form submissions.
        print(request.POST)
        if request.POST.get('status') == "delete":
            try:

                # Deletes user account.
                identity = request.POST.get('delusername')

                status = functions.User_func.Delete(self, identity)
                print(status)
                if status is False:
                    raise Exception("Deletion Failed")

                return render(request, 'accountmanagement.html', {'delete_message': 'Account Deleted Successfully'})
            except Exception as e:
                # Renders account management page with error message.
                return render(request, 'accountmanagement.html',
                              {'message': 'Account Deletion Failed', 'error': str(e)})
        elif request.POST.get('status') == "create":
            try:
                # Creates new user account.



                status = functions.User_func.Create(self, {"username": request.POST.get('username') or False,
                                                           "password": request.POST.get('password') or False,
                                                           "email": request.POST.get('email') or False,
                                                           "name": request.POST.get('name') or False,
                                                           "phone_number": request.POST.get('phone') or False,
                                                           "address": request.POST.get('address') or False,
                                                           "type": request.POST.get('role') or False,
                                                           "skills": '' })
                if status is False:
                    raise Exception("Account not created")
                return render(request, 'accountmanagement.html', {'message': 'Account Created Successfully'})
            except Exception as e:
                # Renders account management page with error message.

                return render(request, 'accountmanagement.html',
                              {'message': "Duplicate username or missing form field"})
        elif request.POST.get('logout') == "Log out":
            # Logs out user.
            logout(request)
            return redirect('/')
        else:
            # Renders account management page with error message.
            return render(request, 'accountmanagement.html', {'message': 'No Account Function Selected'})


class CourseManagement(View):
    def get(self, request):
        # Displays the course management page if user is a supervisor.
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            return render(request, 'coursemanagement.html', {"courses": functions.Course_func.get_all(self), "course_sections": functions.CourseSection_func.get_all(self), "lab_sections": functions.LabSection_func.get_all(self)})
        else:
            # Logs out if user is not authorized.
            logout(request)
            return redirect('/')

    def post(self, request):
        # Handles course management actions.
        if request.POST.get('createcourse') == "true":
            try:
                # Creates new course.
                status = functions.Course_func.Create(self, {"course_id": request.POST.get("courseid") or False,
                                                             "course_name": request.POST.get('name') or False,
                                                             "course_term": request.POST.get('term') or False})
                if status is False:
                    raise Exception("Course not created")
                return render(request, 'coursemanagement.html', {'course_message': 'Course Created Successfully'})
            except Exception as e:
                # Renders course management page with error message.
                return render(request, 'coursemanagement.html',
                              {'create_course': 'Course Creation Failed', 'error': str(e)})
        elif request.POST.get('createcoursesection') == "true":
            try:
                # Creates new course section.
                status = functions.CourseSection_func.Create(self, {"section_id": request.POST.get('sectionid'),
                                                                    "course": request.POST.get('course'),
                                                                    "section_number": request.POST.get('sectionnumber'),
                                                                    "Time": request.POST.get('time'),
                                                                    "Location": request.POST.get('location'),
                                                                    "credits": request.POST.get('credits'),
                                                                    "instructor": request.POST.get('instructor')})
                if status is False:
                    raise Exception("Course Section not created")
                return render(request, 'coursemanagement.html',
                              {'create_course_section_message': 'Course Section Created Successfully'})
            except Exception as e:
                # Renders course management page with error message.
                return render(request, 'coursemanagement.html',
                              {'create_course_section_message': 'Course Section Creation Failed', 'error': str(e)})
        elif request.POST.get('createlabsection') == "true":
            try:
                # Creates new lab section.
                status = functions.LabSection_func.Create(self, {"section_id": request.POST.get('sectionid'),
                                                                 "section_number": request.POST.get('sectionnumber'),
                                                                 "course": request.POST.get('course'),
                                                                 "course_section": request.POST.get('coursesection'),
                                                                 "Time": request.POST.get('time'),
                                                                 "Location": request.POST.get('location'),
                                                                 "Type": request.POST.get('role'),
                                                                 "ta": request.POST.get('ta')})
                if status is False:
                    raise Exception("Lab Section not created")
                return render(request, 'coursemanagement.html', {'lab_message': 'Lab Section Created Successfully'})
            except Exception as e:
                # Renders course management page with error message.
                return render(request, 'coursemanagement.html',
                              {'lab_message': 'Lab Section Creation Failed', 'error': str(e)})
        elif request.POST.get('logout') == "Log out":
            # Logs out user.
            logout(request)
            return redirect('/')
        else:
            # Renders course management page with error message.
            return render(request, 'coursemanagement.html', {'message': 'No Course Function Selected'})


class ViewCourses(View):
    def get(self, request):
        # Displays the view courses page.
        if request.session.get('username'):
            # Populating tables with the database
            courses = functions.Course_func.get_all(self)
            course_sections = functions.CourseSection_func.get_all(self)
            lab_sections = functions.LabSection_func.get_all(self)
            return render(request, 'viewcourses.html',
                          {'courses': courses, 'course_sections': course_sections, 'lab_sections': lab_sections})
        else:
            # Redirects to login if session is not active.
            return redirect('/')

    def post(self, request):
        # Handles logout.
        logout(request)
        return redirect('/')


class ViewUsers(View):
    def get(self, request):
        # Displays the view users page.
        if request.session.get('username'):
            # Populating the table with database
            users = functions.User_func.get_all(self)
            return render(request, 'viewusers.html', {'users': users})
        else:
            # Redirects to login if session is not active.
            return redirect('/')

    def post(self, request):
        # Logs out user.
        logout(request)
        return redirect('/')


class AssignUsers(View):
    def get(self, request):
        # Displays the assign users page and populates select lists.
        names = User.objects.values_list('name', flat=True)
        courses = Course.objects.all()
        section_ids = CourseSection.objects.values_list('section_id', flat=True)
        section_numbers = CourseSection.objects.values_list('section_number', flat=True)

        context = {
            'names': names,
            'courses': courses,
            'section_ids': section_ids,
            'section_numbers': section_numbers,
        }
        return render(request, 'assignusers.html', context)

    def post(self, request):
        # Handles assigning users to courses.
        if request.POST.get('assignuser') == 'true':
            # Extracts form data.
            name = request.POST.get('names')
            course_id = request.POST.get('courseid')
            section_id = request.POST.get('sectionid')
            section_number = request.POST.get('sectionnumber')

            try:
                # Retrieves user, course, and section from the database.
                user = User.objects.get(name=name)
                course = Course.objects.get(course_id=course_id)
                section = course.coursesection_set.get(section_id=section_id, section_number=section_number)

                # Assign user to the course section
                section.instructor = user
                section.save()

                # Rendering a success message
                return render(request, 'assignusers.html', {'message': 'User assigned Successfully'})
            except Exception as e:
                # Handles if user or course doesn't exist
                return render(request, 'assignusers.html', {'message': 'User or Course not found.'})
        elif request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class EditContactInfo(View):
    def get(self, request):

        user = functions.User_func.get(self, "username", request.session.get('username'))

        return render(request, 'editcontactinfo.html', {'oldemail': user[0]['email'], 'oldphone':user[0]['phone_number'], 'oldaddress':user[0]['address']})

    def post(self, request):
        try:

            data = {
                'username': request.session.get('username'),
                'email': request.POST.get('email'),
                'phone_number': request.POST.get('phone'),
                'address': request.POST.get('address')
            }
            print(data)


            status = functions.User_func.Edit(self, data)



            if status is False:
                raise Exception("Error while editing contact info")

            user = functions.User_func.get(self,"username", request.session.get('username'))

             # Displays the edit contact information page.

            return render(request, 'editcontactinfo.html', {'message': "You have successfully edited your contact information", 'oldemail': user[0]['email'], 'oldphone':user[0]['phone_number'], 'oldaddress':user[0]['address']})
        except Exception as e:
          
           # Displays the edit contact information page.
            return render(request, 'editcontactinfo.html', {'message': e})




class Notifications(View):
    def get(self, request):
        # Displays the notifications page.
        return render(request, 'notifications.html')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class InstructorDashboard(View):
    def get(self, request):
        # Displays the instructor dashboard.
        if not request.session.get('username') == "":
            return render(request, 'instructor_dashboard.html', {})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class instructor_edit_contact(View):
    def get(self, request):
        # Displays the instructor edit contact page.
        if request.session.get('username'):
            return render(request, 'instructor_edit_contact.html', {})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class instructor_section_management(View):
    def get(self, request):
        # Displays the instructor section management page.
        if request.session.get('username'):
            return render(request, 'instructor_section_management.html', {})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class instructor_view_courses(View):
    def get(self, request):
        # Displays the instructor view courses page.
        if request.session.get('username'):
            courses = functions.Course_func.get_all(self)
            course_sections = functions.CourseSection_func.get_all(self)
            lab_sections = functions.LabSection_func.get_all(self)
            return render(request, 'instructor_view_courses.html',
                          {'courses': courses, 'course_sections': course_sections, 'lab_sections': lab_sections})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class instructor_view_users(View):
    def get(self, request):
        # Displays the instructor view users page.
        if request.session.get('username'):
            users = User.objects.all()
            return render(request, 'instructor_view_users.html', {'users': users})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class instructor_notifications(View):
    def get(self, request):
        # Displays the instructor notifications page.
        if request.session.get('username'):
            return render(request, 'instructor_notifications.html', {})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class TADashboard(View):
    def get(self, request):
        # Displays the TA dashboard.
        if request.session.get('username'):
            return render(request, 'ta_dashboard.html', {})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class ta_edit_contact(View):
    def get(self, request):
        # Displays the TA edit contact page.
        if request.session.get('username'):
            return render(request, 'ta_edit_contact.html', {})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class ta_my_sections(View):
    def get(self, request):
        # Displays the TA my sections page.
        if request.session.get('username'):
            username = request.session.get('username')
            user = User.objects.get(username=username)
            my_lab_section = functions.LabSection_func.get(self, query='ta', identity=user.id)
            return render(request, 'ta_my_sections.html', {'lab_sections': my_lab_section})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class ta_view_courses(View):
    def get(self, request):
        # Displays the TA view courses page.
        if request.session.get('username'):
            courses = functions.Course_func.get_all(self)
            course_sections = functions.CourseSection_func.get_all(self)
            lab_sections = functions.LabSection_func.get_all(self)
            return render(request, 'ta_view_courses.html',
                          {'courses': courses, 'course_sections': course_sections, 'lab_sections': lab_sections})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')


class ta_view_users(View):
    def get(self, request):
        # Displays the TA view users page.
        if request.session.get('username'):
            users = User.objects.all()
            return render(request, 'ta_view_users.html', {'users': users})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            logout(request)
            return redirect('/')
