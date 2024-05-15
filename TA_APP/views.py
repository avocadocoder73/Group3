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
        if request.POST.get('login') == 'true':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not (username and password):
                return render(request, "login.html", {"message": "Please provide username and password"})
            # check identity
            verify = functions.Login.authenticate(self, str(username), str(password))

            # Redirects to the appropriate dashboard based on user type.
            if verify == 'S':  # Supervisor (or Administrator)
                request.session['username'] = username
                return render(request, 'homepage.html', {"status": "Signed In"})
            elif verify == 'I':  # Instructor
                request.session['username'] = username
                return render(request, 'instructor_dashboard.html', {"status": "Signed In"})
            elif verify == 'T':  # TA
                request.session['username'] = username
                return render(request, 'ta_dashboard.html', {"status": "Signed In"})
            else:
                # Redirects back to login page if authentication fails.
                return render(request, "login.html", {"message": "Username or password is incorrect"})
        else:
            return render(request, "login.html", {"message": ""})


class HomePage(View):
    def get(self, request):
        # Redirects to login if session is not active.
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            return render(request, 'homepage.html', {})
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == 'Log out':
            request.session.pop('username', None)
            return redirect('/')


class AccountManagement(View):
    def get(self, request):
        # Displays the account management page if user is a supervisor.
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            return render(request, 'accountmanagement.html')
        else:
            # Logs out if user is not authorized.
            request.session.pop('username', None)
            return redirect('/')

    def post(self, request):
        # Handles account management form submissions.
        if request.POST.get('status') == "delete":
            try:
                # Deletes user account.
                identity = request.POST.get('delusername')

                status = functions.User_func.Delete(self, identity)
                if status is False:
                    raise Exception("Deletion Failed")

                return render(request, 'accountmanagement.html', {'delete_message': 'Account Deleted Successfully'})
            except Exception as e:
                # Renders account management page with error message.
                return render(request, 'accountmanagement.html',
                              {'delete_message': 'Account Deletion Failed', 'error': str(e)})
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
                                                           "skills": ''})
                if status is False:
                    raise Exception("Account not created")
                return render(request, 'accountmanagement.html', {'message': 'Account Created Successfully'})
            except Exception as e:
                # Renders account management page with error message.
                return render(request, 'accountmanagement.html',
                              {'message': "Duplicate username or missing form field"})
        elif request.POST.get('logout') == "Log out":
            # Logs out user.
            request.session.pop('username', None)
            return redirect('/')
        else:
            # Renders account management page with error message.
            return render(request, 'accountmanagement.html', {'message': 'No Account Function Selected'})


class CourseManagement(View):
    def get(self, request):
        # Displays the course management page if user is a supervisor.
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            return render(request, 'coursemanagement.html', {"courses": functions.Course_func.get_all(self),
                                                             "course_sections": functions.CourseSection_func.get_all(
                                                                 self),
                                                             "lab_sections": functions.LabSection_func.get_all(self)})
        else:
            # Logs out if user is not authorized.
            request.session.pop('username', None)
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
                return render(request, 'coursemanagement.html', {'create_course': 'Course Created Successfully'})
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
        elif request.POST.get('status') == "delete":
            try:
                # Deletes user account.
                identity = request.POST.get('delcourse')

                status = functions.Course_func.Delete(self, identity)
                if status is False:
                    raise Exception("Deletion Failed")

                return render(request, 'coursemanagement.html', {'delete_message': 'Course Deleted Successfully'})
            except Exception as e:
                # Renders account management page with error message.
                return render(request, 'coursemanagement.html',
                              {'delete_message': 'Course Deletion Failed', 'error': str(e)})
        elif request.POST.get('editcourse') == "true":
            try:
                info = {'course_id': request.POST.get('courseid'), 'course_name': request.POST.get('name'),
                        'course_term': request.POST.get('term')}
                status = functions.Course_func.Edit(self, info)
                if status is False:
                    raise Exception("Deletion Failed")

                return render(request, 'coursemanagement.html', {'edit_course_message': 'Course Editing Successful'})
            except Exception as e:
                return render(request, 'coursemanagement.html',
                              {'edit_course_message': 'Course Editing Failed', 'error': str(e)})
        elif request.POST.get('editcoursesection') == "true":
            try:
                instructor = ''
                section_id = request.POST.get('sectionid')
                section = CourseSection.objects.get(section_id=section_id)
                if request.POST.get('instructor'):
                    instructor = User.objects.get(name=request.POST.get('instructor'))
                info = {'section_id': request.POST.get('sectionid'),
                        'Time': request.POST.get('time') or section.Time,
                        'Location': request.POST.get('location') or section.Location,
                        'credits': request.POST.get('credits') or section.credits,
                        'instructor': instructor or section.instructor}
                status = functions.CourseSection_func.Edit(self, info)
                if status is False:
                    raise Exception("Editing Failed")

                return render(request, 'coursemanagement.html',
                              {'edit_course_section_message': 'Course Section Editing Successful'})
            except Exception as e:
                return render(request, 'coursemanagement.html',
                              {'edit_course_section_message': 'Course Section Editing Failed', 'error': str(e)})
        elif request.POST.get('editlabsection') == "true":
            try:
                ta = ''
                section_id = request.POST.get('sectionid')
                section = LabSection.objects.get(section_id=section_id)
                if request.POST.get('ta'):
                    ta = User.objects.get(name=request.POST.get('ta'))
                info = {'section_id': request.POST.get('sectionid'),
                        'Time': request.POST.get('time') or section.Time,
                        'Location': request.POST.get('location') or section.Location,
                        'section_number': request.POST.get('sectionnumber') or section.section_number,
                        'ta': ta or section.ta,
                        'Type': request.POST.get('role') or section.Type}
                status = functions.LabSection_func.Edit(self, info)
                if status is False:
                    raise Exception("Editing Failed")

                return render(request, 'coursemanagement.html',
                              {'edit_lab_section_message': 'Lab Section Editing Successful'})
            except Exception as e:
                return render(request, 'coursemanagement.html',
                              {'edit_lab_section_message': 'Lab Section Editing Failed', 'error': str(e)})
        elif request.POST.get('logout') == "Log out":
            # Logs out user.
            request.session.pop('username', None)
            return redirect('/')
        else:
            # Renders course management page with error message.
            return render(request, 'coursemanagement.html', {'message': 'No Course Function Selected'})


class ViewCourses(View):
    def get(self, request):
        # Displays the view courses page.
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
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
        request.session.pop('username', None)
        return redirect('/')


class ViewUsers(View):
    def get(self, request):
        # Displays the view users page.
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            # Populating the table with database
            users = functions.User_func.get_all(self)
            return render(request, 'viewusers.html', {'users': users})
        else:
            # Redirects to login if session is not active.
            return redirect('/')

    def post(self, request):
        # Logs out user.
        request.session.pop('username', None)
        return redirect('/')


class AssignUsers(View):
    def get(self, request):
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            # Displays the assign users page and populates select lists.
            names = User.objects.values_list('name', flat=True)
            courses = Course.objects.all()
            section_ids = CourseSection.objects.values_list('section_id', flat=True)

            context = {
                'names': names,
                'courses': courses,
                'section_ids': section_ids,
            }
            return render(request, 'assignusers.html', context)
        else:
            return redirect('/')

    def post(self, request):
        # Handles assigning users to courses.
        if request.POST.get('assignuser') == 'true':
            # Extracts form data.
            name = request.POST.get('names')
            course_id = request.POST.get('courseid')
            section_id = request.POST.get('sectionid')
            try:
                # Retrieves user, course, and section from the database.
                user = User.objects.get(name=name)
                if course_id != '':
                    course = Course.objects.get(course_id=course_id)
                    course.assignments.add(user)
                    course.save()
                if section_id != '':
                    section = CourseSection.objects.get(section_id=section_id)
                    section.instructor = user
                    section.save()

                # Rendering a success message
                return render(request, 'assignusers.html', {'message': 'User assigned Successfully'})
            except Exception as e:
                # Handles if user or course doesn't exist
                return render(request, 'assignusers.html', {'message': 'User or Course not found.'})
        elif request.POST.get('logout') == "Log out":
            request.session.pop('username', None)
            return redirect('/')


class EditContactInfo(View):
    def get(self, request):
        if request.session.get('username') and User.objects.get(username=request.session.get('username')).type == 'S':
            user = functions.User_func.get(self, "username", request.session.get('username'))


            context = {
                'oldemail': user[0]['email'],
                'oldphone': user[0]['phone_number'],
                'oldaddress': user[0]['address']
            }

            return render(request, 'editcontactinfo.html', context)
        else:
            return redirect('/')

    def post(self, request):
        if request.POST.get('update_supervisor'):
            try:
                data = {
                    'username': request.session.get('username'),
                    'email': request.POST.get('email'),
                    'phone_number': request.POST.get('phone'),
                    'address': request.POST.get('address')
                }

                status = functions.User_func.Edit(self, data)

                if status is False:
                    raise Exception("Error while editing contact info")

                user = functions.User_func.get(self, "username", request.session.get('username'))

                # Displays the edit contact information page.

                return render(request, 'editcontactinfo.html',
                              {'message': "You have successfully edited your contact information",
                               'oldemail': user[0]['email'], 'oldphone': user[0]['phone_number'],
                               'oldaddress': user[0]['address']})
            except Exception as e:

                # Displays the edit contact information page.
                return render(request, 'editcontactinfo.html', {'message': e})
        elif request.POST.get('logout') == "Log out":
            request.session.pop('username', None)
            return redirect('/')


class Notifications(View):
    def get(self, request):
        # Displays the notifications page.
        return render(request, 'notifications.html')

    def post(self, request):
        # Handles logout.
        if request.POST.get('logout') == "Log out":
            request.session.pop('username', None)
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
            request.session.pop('username', None)
            return redirect('/')


class instructor_edit_contact(View):
    def get(self, request):
        # Displays the instructor edit contact page.
        if request.session.get('username'):
            user = functions.User_func.get(self, "username", request.session.get('username'))
            context = {
                'oldemail': user[0]['email'],
                'oldphone': user[0]['phone_number'],
                'oldaddress': user[0]['address']
            }
            return render(request, 'instructor_edit_contact.html', context)
        else:
            return redirect('/')

    def post(self, request):
        # Handles logout.
        if request.POST.get('update_instructor') == 'true':
            try:
                data = {
                    'username': request.session.get('username'),
                    'email': request.POST.get('email'),
                    'phone_number': request.POST.get('phone'),
                    'address': request.POST.get('address')
                }

                status = functions.User_func.Edit(self, data)

                if status is False:
                    raise Exception("Error while editing contact info")

                user = functions.User_func.get(self, "username", request.session.get('username'))

                # Displays the edit contact information page.

                return render(request, 'instructor_edit_contact.html',
                              {'message': "You have successfully edited your contact information",
                               'oldemail': user[0]['email'], 'oldphone': user[0]['phone_number'],
                               'oldaddress': user[0]['address']})
            except Exception as e:

                # Displays the edit contact information page.
                return render(request, 'instructor_edit_contact.html', {'message': e})
        elif request.POST.get('logout') == "Log out":
            request.session.pop('username', None)
            return redirect('/')


class instructor_section_management(View):
    def get(self, request):
        # Displays the instructor section management page.
        if request.session.get('username'):
            user = functions.User_func.get(self, query='username', identity=request.session.get('username'))
            names = User.objects.filter(type='T')
            courses = functions.Course_func.get_all(self)
            section_ids_course = CourseSection.objects.all()
            section_ids = LabSection.objects.all()

            context = {
                'names': names,
                'courses': courses,
                'section_ids': section_ids,
                'course_section_ids': section_ids_course
            }

            return render(request, 'instructor_section_management.html', context)
        else:
            return redirect('/')

    def post(self, request):
        if request.POST.get('assigncoursesection') == "true":
            name = request.session.get('username')
            course_id = request.POST.get('courseid')
            section_id = request.POST.get('coursesectionid')
            try:
                user = User.objects.get(username=name)
                section = CourseSection.objects.get(section_id=section_id)
                section.instructor = user
                section.save()

                return render(request, 'instructor_section_management.html', {'assign_course_section': 'User assigned Successfully'})
            except Exception as e:
                # Handles if user or course doesn't exist
                return render(request, 'instructor_section_management.html', {'assign_course_section': 'User or Course not found.'})
        elif request.POST.get('assignlabsection') == 'true':
            name = request.POST.get('names')
            course_id = request.POST.get('lab_courseid')
            section_id = request.POST.get('sectionid')
            try:
                user = User.objects.get(name=name)
                section = LabSection.objects.get(section_id=section_id, course_id=course_id)
                section.ta = user
                section.save()

                return render(request, 'instructor_section_management.html', {'assign_lab_section': 'User assigned Successfully'})
            except Exception as e:
                # Handles if user or course doesn't exist
                return render(request, 'instructor_section_management.html', {'assign_lab_section': 'User or Lab section not found'})
        # Handles logout.
        elif request.POST.get('logout') == "Log out":
            request.session.pop('username', None)
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
            request.session.pop('username', None)
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
            request.session.pop('username', None)
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
            request.session.pop('username', None)
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
            request.session.pop('username', None)
            return redirect('/')


class ta_edit_contact(View):
    def get(self, request):
        # Displays the TA edit contact page.
        if request.session.get('username'):
            user = functions.User_func.get(self, "username", request.session.get('username'))
            context = {
                'oldemail': user[0]['email'],
                'oldphone': user[0]['phone_number'],
                'oldaddress': user[0]['address'],
                'oldskills': user[0]['skills']
            }
            return render(request, 'ta_edit_contact.html', context)
        else:
            return redirect('/')

    def post(self, request):
        if request.POST.get('ta_update') == 'true':
            try:
                data = {
                    'username': request.session.get('username'),
                    'email': request.POST.get('email'),
                    'phone_number': request.POST.get('phone'),
                    'address': request.POST.get('address'),
                    'skills': request.POST.get('skills')
                }

                status = functions.User_func.Edit(self, data)

                if status is False:
                    raise Exception("Error while editing contact info")

                user = functions.User_func.get(self, "username", request.session.get('username'))

                # Displays the edit contact information page.
                print(user[0]['skills'])
                return render(request, 'ta_edit_contact.html',
                              {'message': "You have successfully edited your contact information",
                               'oldemail': user[0]['email'], 'oldphone': user[0]['phone_number'],
                               'oldaddress': user[0]['address'], 'oldskills': user[0]['skills']})
            except Exception as e:

                # Displays the edit contact information page.
                return render(request, 'ta_edit_contact.html', {'message': e})
        elif request.POST.get('logout') == "Log out":
            request.session.pop('username', None)
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
            request.session.pop('username', None)
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
            request.session.pop('username', None)
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
            request.session.pop('username', None)
            return redirect('/')
