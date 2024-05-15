import django
from django.core.exceptions import ObjectDoesNotExist
from abc import ABC, abstractmethod
from .models import User, Course, LabSection, CourseSection


class Change(ABC):
    """Create method for general creation"""

    @abstractmethod
    def Create(self, info: dict):
        pass

    """Edit method for general updating"""

    @abstractmethod
    def Edit(self, info: dict):
        pass

    @abstractmethod
    def Delete(self, identity: str):
        pass


class Getting(ABC):
    """General method for getting based on query"""

    @abstractmethod
    def get(self, query: str, identity: str):
        pass

    """General method for getting all instances"""

    @abstractmethod
    def get_all(self):
        pass


class Login:
    """
    Authenticates user login credentials.
    Preconditions: None.
    Postconditions: Returns True if authentication is successful, False otherwise.
    Side Effects: None.
    In: username and password are strings representing user credentials.
    """

    def authenticate(self, username: str, password: str) -> str:
        """Check username"""
        try:
            temp_user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return "No such user"

        """Check is password matches username"""
        if temp_user.password == password:
            if temp_user.type == "I":
                return "I"
            elif temp_user.type == "S":
                return "S"
            elif temp_user.type == "T":
                return "T"
            else:
                return "Invalid user type"
        else:
            return "Invalid password"


class User_func(Change, Getting):
    """
    Create - Creates user based on provided data

    Preconditions: Valid dictionary with correct values based on user.
    Postconditions: User is successfully added to the database.
    Side Effects: Adds a user to database and all locations that reference users.
    In: info - is a dictionary containing user information.
    Out: Boolean - to determine if operation was accomplished or not.
    """

    def Create(self, info: dict) -> bool:
        """Check for empty dictionaries before querying info"""
        if not bool(info):
            return False

        """Check for empty required values before creation"""
        if not ('username' in info and 'password' in info and 'name' in info
                and 'email' in info and 'phone_number' in info and 'address' in info and 'type' in info):
            return False

        if False in info.values():
            return False


        """Check for duplicates"""
        if User.objects.filter(username=info['username']).exists():
            return False

        """Take entries from input dictionary and create a new user"""
        if 'skills' in info:
            """Skills is optional field for creation so check if present"""
            user = User(username=info['username'], password=info['password'], name=info['name'],
                        phone_number=info['phone_number'], email=info['email'], address=info['address'],
                        type=info['type'], skills=info['skills'])

        else:
            user = User(username=info['username'], password=info['password'], name=info['name'],
                        phone_number=info['phone_number'], email=info['email'], address=info['address'],
                        type=info['type'])
        user.save()
        return True

    """
    Edit - Updates user information with the provided data.

    Preconditions: User must be authenticated and exist in the database.
    Postconditions: User information is updated in the database if successful.
    Side Effects: May modify user information in the database and anywhere where user is referenced.
    In: info - is a dictionary containing user information.
    Out: Boolean - to determine if operation was accomplished or not.
    """

    def Edit(self, info: dict) -> bool:
        """Check is username is present"""
        if 'username' not in info:
            return False

        """Check username is in database"""
        try:
            temp_user = User.objects.get(username=info['username'])
        except ObjectDoesNotExist:
            return False

        """Set new password for the user"""
        if 'password' in info:
            temp_user.password = info['password']
            temp_user.save()

        """Set new name for the user"""
        if 'name' in info:
            temp_user.name = info['name']

        """Set new email for the user"""
        if 'email' in info:
            temp_user.email = info['email']

        """Set new phone number for the user"""
        if 'phone_number' in info:
            temp_user.phone_number = info['phone_number']

        """Set new address for the user"""
        if 'address' in info:
            temp_user.address = info['address']

        """Set new type for the user"""
        if 'type' in info:
            temp_user.type = info['type']

        """Set new skills for the user"""
        if 'skills' in info:
            temp_user.skills = info['skills']

        temp_user.save()
        return True

    """
    Delete - Deletes the user from the database.

    Preconditions: User must exist in the database.
    Postconditions: user is removed from the database and everywhere referenced if successful (username,password,etc..).
    Side Effects: Removed from any database tables as a foreign key.
    In: identity - String to locate the given user by username to delete.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Delete(self, identity: str) -> bool:
        """Try and find the user"""
        try:
            temp_user = User.objects.get(username=identity)
        except ObjectDoesNotExist:
            return False

        """delete the user"""
        temp_user.delete()
        return True

    """
    get - Retrieves information about the user(s).

    Preconditions: User(s) must be authenticated and exist in the database.
    Postconditions: Returns a list of dictionaries containing user information (username,password,etc..).
    Side Effects: none
    In: query - string field to search based off of, identity - string fields value to search for
    Out: List - of dictionaries containing the given query
    """

    def get(self, query: str, identity: str) -> list:
        """Create empty lists"""
        return_list = []
        user_list = []

        """Get items based on the given query"""
        match query:
            case "username":
                """find based on username"""
                user_list = User.objects.filter(username=identity).values()
            case "password":
                """find based on password"""
                user_list = User.objects.filter(password=identity).values()
            case "name":
                """find based on name"""
                user_list = User.objects.filter(name=identity).values()
            case "email":
                """find based on email"""
                user_list = User.objects.filter(email=identity).values()
            case "address":
                """find based on address"""
                user_list = User.objects.filter(address=identity).values()
            case "phone_number":
                """find based on phone number"""
                user_list = User.objects.filter(phone_number=identity).values()
            case "type":
                """find based on type"""
                user_list = User.objects.filter(type=identity).values()

        """Go through userlist and create format"""
        for user in user_list:
            temp_dic = {'name': user['name'], 'username': user['username'],
                        'password': user['password'], 'email': user['email'],
                        'phone_number': int(user['phone_number']), 'address': user['address'], 'type': user['type'],
                        'skills': user['skills']}
            """add to list"""
            return_list.append(temp_dic)

        return return_list

    """
    get_all - Retrieves all users from the database.

    Preconditions: None. Will return empty if there is nothing in database.
    Postconditions: Returns a list containing dictionaries of user information.
    Side Effects: None.
    In: None
    Out: List of dictionaries containing all users.
    """

    def get_all(self) -> list:
        """Get all users in table"""
        user_list = User.objects.all()

        """Initialize user list"""
        return_list = []
        """Add entries to list"""
        for user in user_list:
            """create user dictionary"""
            temp_dic = {'name': user.name, 'username': user.username,
                        'password': user.password, 'email': user.email,
                        'phone_number': int(user.phone_number), 'address': user.address, 'type': user.type,
                        'skills': user.skills}
            """add to list"""
            return_list.append(temp_dic)
        """return the list of users"""
        return return_list


class Course_func(Change, Getting):
    """
    Create - Creates course based on provided data

    Preconditions: Valid dictionary with correct values based on course.
    Postconditions: Course is successfully added to the database.
    Side Effects: Adds a course to database and all locations that reference courses.
    In: info is a dictionary containing course information.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Create(self, info: dict) -> bool:
        """Check for empty dictionaries before querying info"""
        if not bool(info):
            return False

        """Check that required fields are present"""
        if not ('course_id' in info and 'course_name' in info and 'course_term' in info):
            return False

        if False in info.values():
            return False

        """Check for duplicates"""
        if Course.objects.filter(course_id=info['course_id']).exists():
            return False

        """Add course to database"""
        course = Course(course_id=info['course_id'], course_name=info['course_name'], course_term=info['course_term'])
        course.save()
        return True

    """
    Edit - Updates course information with the provided data.

    Preconditions: Course must be authenticated and exist in the database.
    Postconditions: Course information is updated in the database if successful.
    Side Effects: May modify user information in the database and anywhere where Course is referenced.
    In: info is a dictionary containing Course information.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Edit(self, info: dict) -> bool:
        """Check is course_id is present"""
        if 'course_id' not in info:
            return False

        """Check course_id is in database"""
        try:
            temp_course = Course.objects.get(course_id=info['course_id'])
        except ObjectDoesNotExist:
            return False

        """Set new course name for the user"""
        if 'course_name' in info:
            temp_course.course_name = info['course_name']
            temp_course.save()

        """Set new course term for the user"""
        if 'course_term' in info:
            temp_course.course_term = info['course_term']
            temp_course.save()

        temp_course.save()
        return True

    """
    Delete - Deletes the Course from the database.

    Preconditions: Course must exist in the database.
    Postconditions: Course is removed from the database and everywhere referenced if successful.
    Side Effects: Removed from any database tables as a foreign key.
    In: String to locate the given Course by course_id to delete.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Delete(self, identity: str) -> bool:
        """Try and find the course"""
        try:
            temp_course = Course.objects.get(course_id=identity)
        except ObjectDoesNotExist:
            return False

        """delete the course"""
        temp_course.delete()
        return True

    """
    get - Retrieves information about the Course(s).

    Preconditions: Course(s) must be authenticated and exist in the database.
    Postconditions: Returns a list of dictionaries containing Course information. (Course_id, Course_name, etc..)
    Side Effects: none
    In: query string field to search based off of, identity fields value to search for
    Out: List of dictionaries containing the given query
    """

    def get(self, query: str, identity: str) -> list:
        """Create empty lists"""
        return_list = []
        course_list = []

        """Term converter"""
        term = {"F": "Fall", "W": "Winter", "Sp": "Spring", "Su": "Summer"}

        """Get items based on the given query"""
        match query:
            case "course_id":
                """find based on course_id"""
                course_list = Course.objects.filter(course_id=identity).values()
            case "course_name":
                """find based on course_name"""
                course_list = Course.objects.filter(course_name=identity).values()
            case "course_term":
                """find based on course_term"""
                """Convert the key"""
                key = [k for k, v in term.items() if v == identity]
                course_list = Course.objects.filter(course_term=key[0]).values()

        """Go through course list and create format"""
        for course in course_list:
            """Statement to fix issue that Django sometimes return the key or the value"""
            if term.get(course["course_term"]) is not None:
                temp_dic = {'course_id': course['course_id'], 'course_name': course['course_name'],
                            'course_term': term[course['course_term']]}
                """add to list"""
            else:
                temp_dic = {'course_id': course['course_id'], 'course_name': course['course_name'],
                            'course_term': course['course_term']}
            return_list.append(temp_dic)

        return return_list

    """
    get_all - Retrieves all Courses from the database.

    Preconditions: None.
    Postconditions: Returns a list containing dictionaries of Course information. (Course_id, Course_name, etc..)
    Side Effects: None.
    In: None
    Out: List of dictionaries containing all Courses.
    """

    def get_all(self) -> list:
        """Get all courses in table"""
        course_list = Course.objects.all()

        """Initialize course list"""
        return_list = []
        """Add entries to list"""
        for course in course_list:
            """create course dictionary"""
            temp_dic = {'course_id': course.course_id, 'course_name': course.course_name,
                        'course_term': course.get_course_term_display()}
            """add to list"""
            return_list.append(temp_dic)
        """return the list of courses"""
        return return_list


class CourseSection_func(Change, Getting):
    """
    Create - Creates CourseSection based on provided data

    Preconditions: Valid dictionary with correct values based on CourseSection.
    Postconditions: CourseSection is successfully added to the database.
    Side Effects: Adds a CourseSection to database and all locations that reference CourseSections.
    In: info is a dictionary containing CourseSection information.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Create(self, info: dict) -> bool:
        # Check if input is empty
        if not info:
            return False

        # Check if all required fields are present
        required_fields = ['section_id', 'course', 'section_number', 'Time', 'Location', 'credits', 'instructor']
        if not all(field in info for field in required_fields):
            return False

        # Check if course section with the given section ID already exists

        if CourseSection.objects.filter(section_id=info['section_id']).exists():
            return False

        # Create and save the new course section
        course_section = CourseSection(section_id=info['section_id'], section_number=info['section_number'],
                                       course=Course.objects.get(course_id=info['course']), Time=info['Time'],
                                       Location=info['Location'], credits=info['credits'],
                                       instructor=User.objects.get(name=info['instructor']))
        course_section.save()

        return True

    """
    Edit - Updates CourseSection information with the provided data.

    Preconditions: CourseSection must be authenticated and exist in the database.
    Postconditions: CourseSection information is updated in the database if successful.
    Side Effects: May modify user information in the database and anywhere where CourseSection is referenced.
    In: info is a dictionary containing CourseSection information.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Edit(self, info: dict) -> bool:
        try:
            # Attempt to retrieve the course section from the database
            course_section = CourseSection.objects.get(section_id=info['section_id'])
            # Update the course section attributes with the provided data
            for key, value in info.items():
                if key == 'instructor':
                    # If the key is 'instructor', retrieve the user object from the database
                    instructor = User.objects.get(username=value)
                    # Set the instructor attribute of the course section to the retrieved user object
                    setattr(course_section, key, instructor)
                else:
                    # Set the attribute of the course section to the provided value
                    setattr(course_section, key, value)
            # Save the updated course section
            course_section.save()
            return True
        except ObjectDoesNotExist:
            # If the course section does not exist in the database, return False
            return False

    """
    Delete - Deletes the CourseSection from the database.

    Preconditions: CourseSection must exist in the database.
    Postconditions: CourseSection is removed from the database and everywhere referenced if successful.
    Side Effects: Removed from any database tables as a foreign key.
    In: String to locate the given CourseSection by section_id to delete.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Delete(self, identity: str) -> bool:
        try:
            # Attempt to retrieve the course section from the database
            course_section = CourseSection.objects.get(section_id=identity)

            # Delete the retrieved course section
            course_section.delete()

            # Return True to indicate successful deletion
            return True
        except ObjectDoesNotExist:
            # If the course section does not exist in the database, return False
            return False

    """
    get - Retrieves information about the CourseSection(s).

    Preconditions: CourseSection(s) must be authenticated and exist in the database.
    Postconditions: Returns a list of dictionaries containing CourseSection information. (Section_id, location, etc..)
    Side Effects: none
    In: query string field to search based off of, identity fields value to search for
    Out: List of dictionaries containing the given query
    """

    def get(self, query: str, identity: str) -> list:
        results = []
        # Check if the query is for section_id
        if query == 'section_id':
            try:
                # Attempt to retrieve the course section from the database using its section_id
                course_section = CourseSection.objects.get(section_id=identity)

                # Construct a dictionary containing the course section information
                result = {
                    'section_id': course_section.section_id,
                    'section_number': course_section.section_number,
                    'course': course_section.course.course_id,
                    'Time': course_section.Time,
                    'Location': course_section.Location,
                    'credits': course_section.credits,
                    'instructor': course_section.instructor.name
                }

                # Return a list containing the constructed dictionary
                return [result]
            except ObjectDoesNotExist:
                # If the course section with the provided section_id does not exist in the database,return an empty list
                return []
        elif query == 'instructor':
            try:
                # Attempt to retrieve the course section from the database using its section_id
                course_sections = CourseSection.objects.all()

                # Construct a dictionary containing the course section information
                for course_section in course_sections:
                    if course_section.instructor.id == identity:
                        result = {
                            'section_id': course_section.section_id,
                            'section_number': course_section.section_number,
                            'course': course_section.course.course_id,
                            'Time': course_section.Time,
                            'Location': course_section.Location,
                            'credits': course_section.credits,
                            'instructor': course_section.instructor.name
                        }
                        results.append(result)
                # Return a list containing the constructed dictionary
                return results
            except ObjectDoesNotExist:
                # If the course section with the provided section_id does not exist in the database,return an empty list
                return []
        else:
            # If the query is not for section_id, return an empty list
            return []

    """
    get_all - Retrieves all CourseSections from the database.

    Preconditions: None.
    Postconditions: Returns a list containing dictionaries of CourseSection information. (Section_id, location, etc..)
    Side Effects: None.
    In: None
    Out: List of dictionaries containing all CourseSections.
    """

    def get_all(self) -> list:
        # Retrieve all course sections from the database
        course_sections = CourseSection.objects.all()

        # Initialize an empty list to store the results
        results = []

        # Iterate over each course section
        for course_section in course_sections:
            # Construct a dictionary containing the course section information
            result = {
                'section_id': course_section.section_id,
                'section_number': course_section.section_number,
                'course': course_section.course.course_id,
                'Time': course_section.Time,
                'Location': course_section.Location,
                'credits': course_section.credits,
                'instructor': course_section.instructor.name
            }

            # Append the constructed dictionary to the results list
            results.append(result)

        # Return the list of results
        return results


class LabSection_func(Change, Getting):
    """
    Create - Creates LabSection based on provided data

    Preconditions: Valid dictionary with correct values based on LabSection.
    Postconditions: LabSection is successfully added to the database.
    Side Effects: Adds a LabSection to database and all locations that reference LabSections.
    In: info is a dictionary containing user information.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Create(self, info: dict) -> bool:
        # Check if input is empty
        if not info:
            return False

        # Check if all required fields are present
        required_fields = ['section_id', 'course', 'section_number', 'Time', 'Location', 'Type', 'ta', 'course_section']
        if not all(field in info for field in required_fields):
            return False

        # Check if lab section with the given section ID already exists
        if LabSection.objects.filter(section_id=info['section_id']).exists():
            return False

        # Create and save the new lab section
        lab_section = LabSection(section_id=info['section_id'], section_number=info['section_number'],
                                 course_section=CourseSection.objects.get(section_id=info['course_section']),
                                 course=Course.objects.get(course_id=info["course"]), Time=info['Time'],
                                 Location=info['Location'], Type=info['Type'], ta=User.objects.get(name=info["ta"]))
        lab_section.save()
        return True

    """
    Edit - Updates LabSection information with the provided data.

    Preconditions: LabSection must be authenticated and exist in the database.
    Postconditions: LabSection information is updated in the database if successful.
    Side Effects: May modify user information in the database and anywhere where LabSection is referenced.
    In: info is a dictionary containing LabSection information.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Edit(self, info: dict) -> bool:
        try:
            # Attempt to retrieve the lab section from the database using its section_id
            lab_section = LabSection.objects.get(section_id=info['section_id'])

            # Iterate over each key-value pair in the info dictionary
            for key, value in info.items():
                # Check if the key is 'ta'
                if key == 'ta':
                    # If key is 'ta', retrieve the User object using the provided username and set it as the value
                    ta = User.objects.get(username=value)
                    setattr(lab_section, key, ta)
                else:
                    # For other keys, set the corresponding attribute of lab_section to the provided value
                    setattr(lab_section, key, value)

            # Save the updated lab section
            lab_section.save()

            # Return True to indicate successful editing
            return True
        except ObjectDoesNotExist:
            # If the lab section with the provided section_id does not exist in the database, return False
            return False

    """
    Delete - Deletes the LabSection from the database.

    Preconditions: LabSection must exist in the database.
    Postconditions: LabSection is removed from the database and everywhere referenced if successful.
    Side Effects: Removed from any database tables as a foreign key.
    In: String to locate the given LabSection by section_id to delete.
    Out: Boolean to determine if operation was accomplished or not.
    """

    def Delete(self, identity: str) -> bool:
        try:
            # Attempt to retrieve the lab section from the database using its section_id
            lab_section = LabSection.objects.get(section_id=identity)

            # Delete the retrieved lab section from the database
            lab_section.delete()

            # Return True to indicate successful deletion
            return True
        except ObjectDoesNotExist:
            # If the lab section with the provided section_id does not exist in the database, return False
            return False

    """
    get - Retrieves information about the LabSection(s).
    
    Preconditions: LabSection(s) must be authenticated and exist in the database.
    Postconditions: Returns a list of dictionaries containing LabSection information. (Section_id, location, etc..)
    Side Effects: none
    In: query string field to search based off of, identity fields value to search for
    Out: List of dictionaries containing the given query
    """

    def get(self, query: str, identity: str) -> list:
        results = []
        # Check if the query is for section_id
        if query == 'section_id':
            try:
                # Attempt to retrieve the lab section from the database using its section_id
                lab_section = LabSection.objects.get(section_id=identity)

                # Convert the LabSection instance to a dictionary
                result = {
                    'section_id': lab_section.section_id,
                    'section_number': lab_section.section_number,
                    'course_section': lab_section.course_section.section_id,
                    'course': lab_section.course.course_id,
                    'Time': lab_section.Time,
                    'Location': lab_section.Location,
                    'Type': lab_section.Type,
                    'ta': lab_section.ta.name
                }

                # Return a list containing the constructed dictionary
                return [result]
            except ObjectDoesNotExist:
                # If the lab section with the provided section_id does not exist in the database, return an empty list
                return []
        elif query == 'ta':
            try:
                # Attempt to retrieve the lab section from the database using its ta
                lab_section = LabSection.objects.all()
                # Convert the LabSection instance to a dictionary
                for lab in lab_section:
                    if lab.ta.id == identity:
                        result = {
                            'section_id': lab.section_id,
                            'section_number': lab.section_number,
                            'course_section': lab.course_section.section_id,
                            'course': lab.course.course_id,
                            'Time': lab.Time,
                            'Location': lab.Location,
                            'Type': lab.Type,
                            'ta': lab.ta.name
                        }
                        results.append(result)
                # Return a list containing the constructed dictionary
                return results
            except ObjectDoesNotExist:
                # If the lab section with the provided section_id does not exist in the database, return an empty list
                return []
        else:
            return []


    """
    get_all - Retrieves all LabSections from the database.

    Preconditions: None.
    Postconditions: Returns a list containing dictionaries of LabSection information. (Section_id, location, etc..)
    Side Effects: None.
    In: None
    Out: List of dictionaries containing all LabSections.
    """

    def get_all(self) -> list:
        # Retrieve all lab sections from the database
        lab_sections = LabSection.objects.all()

        # Initialize an empty list to store the results
        results = []

        # Iterate over each lab section retrieved from the database
        for lab_section in lab_sections:
            # Convert the lab section instance to a dictionary and append it to the results list
            result = {
                'section_id': lab_section.section_id,
                'section_number': lab_section.section_number,
                'course_section': lab_section.course_section.section_id,
                'course': lab_section.course.course_id,
                'Time': lab_section.Time,
                'Location': lab_section.Location,
                'Type': lab_section.Type,
                'ta': lab_section.ta.name
            }
            results.append(result)

        # Return the list of dictionaries containing information about all lab sections
        return results


"""Notification class for sending notifications"""


class Notify():
    """
    email. Sends an email based on the given txt file

    Preconditions: string Txt file name contains valid information for sending an email.
    Postconditions: Sends an email to a recipient. Returns a bool if it works well.
    Side Effects: None.
    In: filename: str for file name contains information
    Out: bool if the operations fails or not
    """

    """"!!! This is an email code I have from a previous project since it was not part of our scope this sprint 
             I put it in for what emailing implementation could look like."""
    def email(self,filename:str) -> bool:
        """with open(arg,encoding="utf-8") as f:
            #Input file lines to read from
            contents = f.readlines()
            con_email = contents[1].split("@",1)
            #print(contents)
            if len(con_email) != 1:
                #Domain to send to
                con_domain = con_email[1].split(">",1)[0]
            else:
                #If there is a wrong formating with no @ in email address
                print("Input email is formatted wrong.")
                return False
            #Format the email from
            from_email = contents[0].split("<")[1]
            from_email = from_email.split(">")[0]
            from_body = f"MAIL FROM: <{from_email}>\r\n"
            #Format the email to
            to_email = contents[1].split("<")[1]
            to_email = to_email.split(">")[0]
            to_body = f"RCPT TO: <{to_email}>\r\n"
            #Format the subject
            subject = contents[2].split("\n")[0]
            #Format the body
            message_body = contents[4]
        #Get the output from the terminal command
        with Popen(f"nslookup -q=MX {con_domain}",shell=True,stdout=PIPE,stderr=PIPE) as ter_out:
            output, error = ter_out.communicate()
        if error.find(b"Non-existent domain") != -1:
            #If the domain deos not exsist we will not be sending an email to it
            print("Domain does not exists %s",con_domain)
            return False
        #Find the mail server
        MAIL_SERVER = b''
        MX = output.split(b"mail exchanger = ",1)
        if len(MX)>1:
            MAIL_SERVER = MX[1].split(b"\r\n",1)[0]
        else:
            print("Mail Exchange server not found.")
            return False
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s_stream:
            #Connect to SMTP server
            s_stream.connect((MAIL_SERVER,25))
            connect_ret = s_stream.recv(1024)
            #Send hello to server
            #print(connect_ret)
            HELLO = "HELO Nick\r\n"
            s_stream.send(HELLO.encode())
            hello_ret = s_stream.recv(1024)
            #print(hello_ret)
            #Mail sender
            s_stream.send(from_body.encode())
            from_ret = s_stream.recv(1024)
            #print(from_ret)
            #Mail receiver
            s_stream.send(to_body.encode())
            recv_ret = s_stream.recv(1024)
            if recv_ret.find(b"501") ==0 or recv_ret.find(b"503") ==0 or recv_ret.find(b"550") == 0:
                print("Recipient does not exist in this domain: %s",con_domain)
                return False
            #print(recv_ret)
            #Ask to send data
            s_stream.send(b"DATA\r\n")
            data_ret = s_stream.recv(1024)
            #print(data_ret)
            #Send message
            message=f"From:{from_email}\r\nTo:{to_email}
            \r\n{subject}\r\n\r\n{message_body}\r\n.\r\n"
            s_stream.send(message.encode())
            message_ret = s_stream.recv(1024)
            if message_ret.find(b'250') != -1:
                print("Successfully sent email to %s",to_email)
                return True
            """