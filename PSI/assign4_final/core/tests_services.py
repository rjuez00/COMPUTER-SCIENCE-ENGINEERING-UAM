# code creat4ed by R. Marabini
import re
from decimal import Decimal
import datetime

from django.utils import timezone
from django.test import Client, TestCase
from django.urls import reverse

from core.management.commands.populate import Command
from core.models import (Student, OtherConstraints,
                         Pair, TheoryGroup, GroupConstraints,
                         LabGroup)

###################
# You may modify the following variables

# students ids began in this number
# this avoid conflicts with superuser
FIRST_STUDENT_ID = 1000

USERNAME_1 = "testUser_1"
PASSWORD_1 = "pass1"
FIRST_NAME_1 = "user1"
LAST_NAME_1 = "name1"
USERNAME_2 = "testUser_2"
PASSWORD_2 = "pass2"
FIRST_NAME_2 = "user2"
LAST_NAME_2 = "name2"
USERNAME_3 = "testUser_3"
PASSWORD_3 = "pass3"
FIRST_NAME_3 = "user3"
LAST_NAME_3 = "name3"
USERNAME_4 = "testUser_4"
PASSWORD_4 = "pass4"
FIRST_NAME_4 = "user4"
LAST_NAME_4 = "name4"

USER_SESSION_ID = "_auth_user_id"

LOGIN_SERVICE = "login"
LOGOUT_SERVICE = "logout"
LOGIN_TITLE = "Login"

LANDING_TITLE = r"Home"  # redirect here after login
LANDING_PAGE = "home"

CONVALIDATION_SERVICE = 'convalidation'
CONVALIDATION_TITLE = 'Convalidation'

PAIR_SERVICE = "applypair"
PAIR_TITLE = 'Apply Pair'
PAIR_SAME_USER = 'User has already selected a pair'
PAIR_FORM_LABEL = 'student'
PAIR_SELECTION_ERROR = 'Error getting pair'
BREAK_SERVICE = "breakpair"
BREAK_TITLE = 'Break Pair'
BREAK_FORM_LABEL = 'pair'

GROUP_SERVICE = "applygroup"
GROUP_TITLE = 'Apply Group'
GROUP_FORM_LABEL = 'group'
GROUP_ERROR_NOT_VALID = 'Members of the theory group'

SERVICE_DEF = {LOGIN_SERVICE: {
        "title": LOGIN_TITLE,
        "pattern": r"Please login|Por favor autentiquese"
    },
    LANDING_PAGE: {
        "title": LANDING_TITLE,
        # search pattern "Hi <b> plus any string composed by [a-zA-Z0-9_]
        "pattern": r"Summary page for <b>(?P<username>\w+)"
    },
    CONVALIDATION_SERVICE: {
        "title": CONVALIDATION_TITLE,
        "patternfail": r"do not satisfy",
        "pattern": r"You satisfy requirements."
    },
    PAIR_SERVICE: {
        "title": PAIR_TITLE,
        "pattern": r"Select the second"
    },
    BREAK_SERVICE: {
        "title": BREAK_TITLE,
        "pattern": r"Select the pair to be"
    },
    GROUP_SERVICE: {
        "title": GROUP_TITLE,
        "patternfail": r"Group selection is not active",
        "pattern": r"Select the group you want to join to"
    },
}
# PLease do not modify anything below this line
###################

# TODO: Student class inherits from User
# class Student(User):


class ServiceBaseTest(TestCase):
    def setUp(self):
        self.paramsUser1 = {"username": USERNAME_1,
                            "password": PASSWORD_1,
                            "first_name": FIRST_NAME_1,
                            "last_name": LAST_NAME_1,
                            "id": FIRST_STUDENT_ID}
        self.paramsUser2 = {"username": USERNAME_2,
                            "password": PASSWORD_2,
                            "first_name": FIRST_NAME_2,
                            "last_name": LAST_NAME_2,
                            "id": FIRST_STUDENT_ID+1}
        self.paramsUser3 = {"username": USERNAME_3,
                            "password": PASSWORD_3,
                            "first_name": FIRST_NAME_3,
                            "last_name": LAST_NAME_3,
                            "id": FIRST_STUDENT_ID+2}
        self.paramsUser4 = {"username": USERNAME_4,
                            "password": PASSWORD_4,
                            "first_name": FIRST_NAME_4,
                            "last_name": LAST_NAME_4,
                            "id": FIRST_STUDENT_ID+3}

        self.user1 = Student.objects.create_user(
            id=self.paramsUser1["id"],
            username=self.paramsUser1["username"],
            password=self.paramsUser1["password"],
            first_name=self.paramsUser1["first_name"],
            last_name=self.paramsUser1["last_name"])
        self.user2 = Student.objects.create_user(
            id=self.paramsUser2["id"],
            username=self.paramsUser2["username"],
            password=self.paramsUser2["password"],
            first_name=self.paramsUser2["first_name"],
            last_name=self.paramsUser2["last_name"])
        self.user3 = Student.objects.create_user(
            id=self.paramsUser3["id"],
            username=self.paramsUser3["username"],
            password=self.paramsUser3["password"],
            first_name=self.paramsUser3["first_name"],
            last_name=self.paramsUser3["last_name"])
        self.user4 = Student.objects.create_user(
            id=self.paramsUser4["id"],
            username=self.paramsUser4["username"],
            password=self.paramsUser4["password"],
            first_name=self.paramsUser4["first_name"],
            last_name=self.paramsUser4["last_name"])

        self.client1 = self.client
        self.client2 = Client()
        self.client3 = Client()
        self.populate = Command()
        self.populate.teacher()
        self.populate.otherconstrains()
        self.populate.theorygroup()
        self.populate.labgroup()
        self.populate.groupconstraints()

    def tearDown(self):
        self.populate.cleanDataBase()

    @classmethod
    def loginTestUser(cls, client, user):
        client.force_login(user)

    @classmethod
    def logoutTestUser(cls, client):
        client.logout()

    @classmethod
    def decode(cls, txt):
        return txt.decode("utf-8")

    def validate_login_required(self, client, service):
        self.logoutTestUser(client)
        response = client.get(reverse(service), follow=True)
        self.assertEqual(response.status_code, 200)
        self.is_login(response)

    def validate_response(self, service, response, fail=False):
        definition = SERVICE_DEF[service]
        self.assertRegex(self.decode(response.content), definition["title"])
        if fail:
            # print(definition["patternfail"], self.decode(response.content))
            m = re.search(definition["patternfail"],
                          self.decode(response.content))
        else:
            # print(definition["pattern"], self.decode(response.content))
            m = re.search(definition["pattern"], self.decode(response.content))
        self.assertTrue(m)
        return m

    def is_login(self, response):
        self.validate_response(LOGIN_SERVICE, response)

    def is_request_pair(self, response):
        self.validate_response(PAIR_SERVICE, response)

    def is_convalidated(self, reponse, fail=False):
        self.validate_response(CONVALIDATION_SERVICE, reponse, fail)

    def is_landing_autenticated(self, response, user):
        m = self.validate_response(LANDING_PAGE, response)
        self.assertEqual(m.group("username"), user.first_name)

    def is_break_pair(self, response):
        self.validate_response(BREAK_SERVICE, response)

    def is_group(self, response, fail=False):
        self.validate_response(GROUP_SERVICE, response, fail)


class LogInOutServiceTests(ServiceBaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test01_log_page(self):
        "check log page but do not log in"
        # check that no student is loged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # call "login" service and check that "login" is in the title
        # LOGIN_SERVICE should match the label for your login url
        response = self.client1.get(reverse(LOGIN_SERVICE), follow=True)
        self.assertEqual(response.status_code, 200)
        # so far we have just connect to the login page
        # but we have not login so no user should be active
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # check that the strings  SERVICE_DEF[LOGIN_SERVICE]
        # "title" and "pattern" are shown
        self.is_login(response)

    def test02_log_in(self):
        "login and validate login page"
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE), self.paramsUser1,
                          follow=True)
        # check students ids are correct
        self.assertEqual(Decimal(self.client1.session.get(USER_SESSION_ID)),
                         self.user1.id)
        # connect to login page from another client/browser
        self.validate_login_required(self.client2, LOGIN_SERVICE)
        # check that for these second broewser point of view no
        # student has logged in
        self.assertFalse(self.client2.session.get(USER_SESSION_ID, False))

    def test03_log_in_two_users(self):
        """log in with 2 different users from two different
        clients/browsers"""
        sessions = [
            {"client": self.client1, "user": self.user1},
            {"client": self.client2, "user": self.user2}
        ]

        for session in sessions:
            self.loginTestUser(session["client"], session["user"])

        for session in sessions:
            response = session["client"].get(reverse(LANDING_PAGE),
                                             follow=True)
            self.is_landing_autenticated(response, session["user"])

    def test04_logout(self):
        "log in, then log out and test that user is not logged in"
        # login
        self.loginTestUser(self.client1, self.user1)
        # test user loggedin
        self.assertEqual(Decimal(self.client1.session.get(USER_SESSION_ID)),
                         self.user1.id)
        # logged out
        self.client1.get(reverse(LOGOUT_SERVICE), follow=True)
        # test user is logged out
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))

    def test05_log_in_apir(self):
        "login and validate login page when a Pair exists"
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # create pair
        p = Pair(student1=self.user1, student2=self.user2)
        p.save()
        # log in
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.paramsUser1,
                                     follow=True)
        self.assertFalse(self.decode(response.content).
                         find(self.user2.first_name) == -1)


class ConvalidationServiceTests(ServiceBaseTest):
    "Test related with convalidation "
    def test10_convalidation_fail(self):
        # create user that will not pass convalidation
        # add grades
        self.user1.gradeTheoryLastYear = 2.9
        self.user1.gradeLabLastYear = 8
        self.user1.save()
        # login
        self.loginTestUser(self.client1, self.user1)
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        # convalidation test
        self.is_convalidated(response, fail=True)

    def test11_convalidation_sucess(self):
        # create user that will pass convalidation
        # add grades
        self.user1.gradeTheoryLastYear = 4.0
        self.user1.gradeLabLastYear = 8
        self.user1.save()
        # login
        self.loginTestUser(self.client1, self.user1)
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        # convalidation test
        self.is_convalidated(response, fail=False)

    def test12_convalidation_no_login(self):
        # try to convalidate without login first
        # logout
        self.client1.get(reverse(LOGOUT_SERVICE), follow=True)
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        self.is_login(response)

    def test13_convalidation_member1_pair(self):
        """try to convalidate when you are member of a pair
        as student1"""
        self.loginTestUser(self.client1, self.user1)
        p = Pair(student1=self.user1, student2=self.user2)
        p.save()
        self.user1.gradeTheoryLastYear = 4.0
        self.user1.gradeLabLastYear = 8
        self.user1.save()
        # refresh user1
        self.user1 = Student.objects.get(pk=self.user1.id)
        self.assertFalse(self.user1.convalidationGranted)
        self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        self.assertFalse(self.user1.convalidationGranted)
        Pair.objects.all().delete()
        self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        # refresh user1
        self.user1 = Student.objects.get(pk=self.user1.id)
        self.assertTrue(self.user1.convalidationGranted)

    def test14_convalidation_member1_pair(self):
        """try to convalidate when you are member of a pair
        as student2 and the pair is convalidated"""
        self.loginTestUser(self.client2, self.user2)
        p = Pair(student1=self.user1,
                 student2=self.user2,
                 validated=True)
        p.save()
        self.user2.gradeTheoryLastYear = 4.0
        self.user2.gradeLabLastYear = 8
        self.user2.save()
        # refresh user2
        self.user2 = Student.objects.get(pk=self.user2.id)
        self.assertFalse(self.user2.convalidationGranted)
        self.client2.get(reverse(CONVALIDATION_SERVICE),
                         follow=True)
        self.assertFalse(self.user2.convalidationGranted)
        p.validated=False
        p.save()
        self.client2.get(reverse(CONVALIDATION_SERVICE),
                         follow=True)
        # refresh user2
        self.user2 = Student.objects.get(pk=self.user2.id)
        self.assertTrue(self.user2.convalidationGranted)


class PairServiceTests(ServiceBaseTest):
    """ Test related with the creation of pairs"""
    def test20_pair(self):
        """test pair creation:
        a) URL PAIR_SERVICE exists
        b) list with potential users exists
        c) logged user is not in the list of potential users
        d) Pair object is saved properly with
           student1, student2 and validation = False
        e) It is not possible to connect to URL without login first
        """
        # login 1 user
        self.loginTestUser(self.client1, self.user1)
        # ask for pair page
        response = self.client1.get(reverse(PAIR_SERVICE), follow=True)
        # check landing page is OK
        self.is_request_pair(response)
        # check list of users is OK
        m = re.search(self.user2.first_name, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(self.user1.first_name, self.decode(response.content))
        self.assertFalse(m)
        # check result of pressing submit is OK
        # need to pass a POST calling to PAIR_SERVICE
        data = {PAIR_FORM_LABEL: FIRST_STUDENT_ID + 1}
        self.client1.post(reverse(PAIR_SERVICE),
                          data=data,
                          follow=True)

        self.assertTrue(Pair.objects.filter(student1=self.user1).exists())
        self.assertTrue(Pair.objects.filter(student2=self.user2).exists())
        self.assertFalse(Pair.objects.filter(student1=self.user2).exists())
        self.assertTrue(Pair.objects.filter(validated=False).exists())
        self.assertFalse(Pair.objects.filter(validated=True).exists())
        # try to connect to page with no login
        self.client1.get(reverse(LOGOUT_SERVICE), follow=True)
        self.client1.get(reverse(PAIR_SERVICE), follow=True)
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        self.is_login(response)

    def test21_double_pair(self):
        """A single user should not be able to create
           two Pairs with same user"""
        # user1 logs in
        self.loginTestUser(self.client1, self.user1)
        # go to apply pair page
        # response = self.client1.get(reverse(PAIR_SERVICE), follow=True)
        data = {PAIR_FORM_LABEL: FIRST_STUDENT_ID+1}
        # create pair user1 & user 2
        self.assertTrue(len(Pair.objects.all()) == 0)
        response = self.client1.post(reverse(PAIR_SERVICE),
                                     data=data,
                                     follow=True)
        # test new pair has been created
        self.assertTrue(len(Pair.objects.all()) == 1)
        # try to create a second page using the same user
        data = {PAIR_FORM_LABEL: FIRST_STUDENT_ID+2}
        response = self.client1.post(reverse(PAIR_SERVICE),
                                     data=data,
                                     follow=True)
        # check no new pair has been created
        self.assertTrue(len(Pair.objects.all()) == 1,
                        "Two pairs created by the same user")
        # check error message
        m = re.search(PAIR_SAME_USER, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(SERVICE_DEF[PAIR_SERVICE]["pattern"],
                      self.decode(response.content))
        self.assertFalse(m)

    def test22_validate_pair(self):
        """validate pair:
        (a) user1 request pair
            pair is created with validate = False
        (b) user 2 request same pair
            validate is set to True and no new pair is created
        """
        self.loginTestUser(self.client1, self.user1)
        self.loginTestUser(self.client2, self.user2)
        # create first request
        data = {PAIR_FORM_LABEL: FIRST_STUDENT_ID+1}
        # create pair user1 & user 2
        # check that no Pair exists
        self.assertTrue(len(Pair.objects.all()) == 0)
        self.client1.post(reverse(PAIR_SERVICE),
                          data=data,
                          follow=True)
        # test new pair has been created with validate set to false
        self.assertTrue(len(Pair.objects.all()) == 1)
        p = Pair.objects.all().first()
        self.assertFalse(p.validated)
        # create second request
        data = {PAIR_FORM_LABEL: FIRST_STUDENT_ID}
        # create pair user2 & user 1
        self.client2.post(reverse(PAIR_SERVICE),
                          data=data,
                          follow=True)
        # test no new pair has been created
        self.assertTrue(len(Pair.objects.all()) == 1)
        # but validate has been changed
        p = Pair.objects.all().first()
        self.assertTrue(p.validated)

    def test23_do_not_offer_validated_user(self):
        """Test that when creating a pair
         users in validated pairs are not offered"""
        # first request
        self.loginTestUser(self.client1, self.user1)
        response = self.client1.get(reverse(PAIR_SERVICE), follow=True)
        m = re.search(">%s," % LAST_NAME_2, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(">%s," % LAST_NAME_3, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(">%s," % LAST_NAME_4, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(">%s," % LAST_NAME_1, self.decode(response.content))
        self.assertFalse(m)
        data = {PAIR_FORM_LABEL: FIRST_STUDENT_ID+1}
        self.client1.post(reverse(PAIR_SERVICE),
                          data=data,
                          follow=True)
        # second request
        self.loginTestUser(self.client2, self.user2)
        data = {PAIR_FORM_LABEL: FIRST_STUDENT_ID}
        self.client2.post(reverse(PAIR_SERVICE),
                          data=data,
                          follow=True)
        self.client1.get(reverse(LOGOUT_SERVICE), follow=True)
        self.client2.get(reverse(LOGOUT_SERVICE), follow=True)
        # login user3
        self.loginTestUser(self.client1, self.user3)
        response = self.client1.get(reverse(PAIR_SERVICE), follow=True)
        m = re.search(">%s," % LAST_NAME_2, self.decode(response.content))
        self.assertFalse(m)
        m = re.search(">%s," % LAST_NAME_3, self.decode(response.content))
        self.assertFalse(m)
        m = re.search(">%s," % LAST_NAME_4, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(">%s," % LAST_NAME_1, self.decode(response.content))
        self.assertFalse(m)


class BreakPairServiceTests(ServiceBaseTest):
    "test related with breaking pairs"
    def test30_breakpair_no_login(self):
        "try to breakpair without login first"
        # logout"
        self.client1.get(reverse(LOGOUT_SERVICE), follow=True)
        response = self.client1.get(reverse(BREAK_SERVICE), follow=True)
        self.is_login(response)

    def test31_novalidated_breakpair(self):
        """test break pair simple case:
        a) login
        b) created NOT validated pair
        c) break pair
        """
        # create simple pair
        # with validated = False
        p = Pair(student1=self.user1, student2=self.user2)
        p.save()
        pid = p.id
        # login 1 user
        self.loginTestUser(self.client1, self.user1)
        # ask for break page
        response = self.client1.get(reverse(BREAK_SERVICE), follow=True)
        # check landing page is OK
        self.is_break_pair(response)
        # check list of users is OK
        m = re.search(self.user1.first_name, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(self.user2.first_name, self.decode(response.content))
        self.assertTrue(m)
        m = re.search(self.user3.first_name, self.decode(response.content))
        self.assertFalse(m)
        m = re.search(self.user4.first_name, self.decode(response.content))
        self.assertFalse(m)
        # POST call to BREAK_SERVICE
        data = {BREAK_FORM_LABEL: pid}
        response = self.client1.post(reverse(BREAK_SERVICE),
                                     data=data,
                                     follow=True)
        self.assertFalse(Pair.objects.filter(pk=pid).exists())

    def test32_validated_breakpair_first_user(self):
        """test break pair simple case:
        a) login
        b) created NOT validated pàir
        c) break pair
        """
        # create simple pair
        # with validated = False
        p = Pair(student1=self.user1, student2=self.user2, validated=True)
        p.save()
        pid = p.id
        # login 2 users
        self.loginTestUser(self.client1, self.user1)
        self.loginTestUser(self.client2, self.user2)
        self.assertIsNone(Pair.objects.get(pk=pid).studentBreakRequest)
        # POST call to BREAK_SERVICE
        # user1
        data = {BREAK_FORM_LABEL: pid}
        self.client1.post(reverse(BREAK_SERVICE),
                          data=data,
                          follow=True)
        self.assertTrue(Pair.objects.filter(pk=pid).exists())
        # check studentBreak is active
        self.assertTrue(Pair.objects.get(pk=pid).studentBreakRequest ==
                        self.user1)
        # user2
        self.client2.post(reverse(BREAK_SERVICE),
                          data=data,
                          follow=True)
        # check pair has been deleted
        self.assertFalse(Pair.objects.filter(pk=pid).exists())

    def test33_validated_breakpair_second_user(self):
        """As previous cse but user 2 beaks the pair
        """
        # create simple pair
        # with validated = True
        p = Pair(student1=self.user1, student2=self.user2, validated=True)
        p.save()
        pid = p.id
        # login 2 users
        self.loginTestUser(self.client1, self.user1)
        self.loginTestUser(self.client2, self.user2)
        self.assertIsNone(Pair.objects.get(pk=pid).studentBreakRequest)
        # POST call to BREAK_SERVICE
        # user2
        data = {BREAK_FORM_LABEL: pid}
        self.client2.post(reverse(BREAK_SERVICE),
                          data=data,
                          follow=True)
        self.assertTrue(Pair.objects.filter(pk=pid).exists())
        # check studentBreak is active
        self.assertTrue(Pair.objects.get(pk=pid).studentBreakRequest ==
                        self.user2)
        # user1
        self.client1.post(reverse(BREAK_SERVICE),
                          data=data,
                          follow=True)
        # check pair has been deleted
        self.assertFalse(Pair.objects.filter(pk=pid).exists())

    def test34_validated_breakpair_user_twice_requested(self):
        """user 1 and user 2 has requested user 3 as pair
        user 3 has accepted user 2 request
        break all pairs
        """
        # first pair with  validated = False
        p = Pair(student1=self.user1, student2=self.user3, validated=False)
        p.save()
        p1id = p.id
        # second pair with  validated = True
        p = Pair(student1=self.user2, student2=self.user3, validated=True)
        p.save()
        p2id = p.id

        # login 3 users
        self.loginTestUser(self.client1, self.user1)
        self.loginTestUser(self.client2, self.user2)
        self.loginTestUser(self.client3, self.user3)

        # assert pairs
        self.assertIsNone(Pair.objects.get(pk=p1id).studentBreakRequest)
        self.assertIsNone(Pair.objects.get(pk=p2id).studentBreakRequest)
        # POST call to BREAK_SERVICE
        # user2 tries to break second pair
        data = {BREAK_FORM_LABEL: p2id}
        self.client2.post(reverse(BREAK_SERVICE),
                          data=data,
                          follow=True)
        # but will not be broken until user3 breaks it too
        self.assertTrue(Pair.objects.filter(pk=p2id).exists())
        # check studentBreak is active
        self.assertTrue(Pair.objects.get(pk=p2id).studentBreakRequest ==
                        self.user2)
        # user 1 break pair, since it is not validated is OK
        data = {BREAK_FORM_LABEL: p1id}
        self.client1.post(reverse(BREAK_SERVICE),
                          data=data,
                          follow=True)
        # check pair has been deleted
        self.assertFalse(Pair.objects.filter(pk=p1id).exists())

        # finally user 3 breaks second pair
        data = {BREAK_FORM_LABEL: p2id}
        self.client3.post(reverse(BREAK_SERVICE),
                          data=data,
                          follow=True)
        # check pair has been deleted
        self.assertFalse(Pair.objects.filter(pk=p2id).exists())

    def test35_break_nonexisting_pair(self):
        """test pair that does not exists
        """
        # login
        self.loginTestUser(self.client1, self.user1)
        # send wrong pait id
        data = {BREAK_FORM_LABEL: 123456}
        response = self.client1.post(reverse(BREAK_SERVICE),
                                     data=data,
                                     follow=True)
        self.assertFalse(
            self.decode(response.content).find(PAIR_SELECTION_ERROR)==-1)


class GroupServiceTests(ServiceBaseTest):
    "Test related with applying for a group"

    def test40_apply_group_no_login(self):
        "try to apply for a group without login first"
        # logout
        self.client1.get(reverse(LOGOUT_SERVICE), follow=True)
        # apply for a group
        response = self.client1.get(reverse(GROUP_SERVICE), follow=True)
        # the returned page should be login page
        self.is_login(response)

    def test_41_select_group_before_time(self):
        """ Test page for group selection before deadline
         Note that use must be informed if selection is not active """
        # login
        self.loginTestUser(self.client1, self.user1)
        # set othercostraint.selectGroupStart to now plus 1 day
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now + datetime.timedelta(1)
        o.save()
        # connect to create group page
        response = self.client1.get(reverse(GROUP_SERVICE), follow=True)
        self.is_group(response, fail=True)

    def test_42_select_group_no_pair(self):
        """ select group for user with no pair """
        # login
        self.loginTestUser(self.client1, self.user1)
        # get all theory groups
        tgQS = TheoryGroup.objects.all()
        # set othercostraint.selectGroupStart to now
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now
        o.save()
        # pick valid groups
        # for each theory group
        for theoryGroup in tgQS:
            print(theoryGroup.groupName)
            self.user1.theoryGroup = theoryGroup
            self.user1.save()
            # connect to create group page
            response = self.client1.get(reverse(GROUP_SERVICE), follow=True)
            # check labgroups offered are right
            gcQS = GroupConstraints.objects.filter(theoryGroup=theoryGroup)
            for groupConstraint in gcQS:
                print("    ", groupConstraint.labGroup.groupName)
                m = re.search(groupConstraint.labGroup.groupName,
                              self.decode(response.content))
                self.assertTrue(m)
        # try to create all groups with all possible combination
        # Theory group, labgroup. some should be invalid
        # use html page instead of function to select groups
        tgQS = TheoryGroup.objects.all()
        lgQS = LabGroup.objects.all()

        for theoryGroup in tgQS:
            for labGroup in lgQS:
                self.user1.theoryGroup = theoryGroup
                self.user1.save()
                labGroupId = labGroup.id
                data = {GROUP_FORM_LABEL: labGroupId}
                counter = labGroup.counter
                self.client1.post(reverse(GROUP_SERVICE),
                                  data=data,
                                  follow=True)
                valid = GroupConstraints.objects.filter(
                    theoryGroup=theoryGroup,
                    labGroup=labGroup).exists()
                if valid:
                    print(theoryGroup.groupName, "-->",
                          labGroup.groupName, ", valid")
                    self.assertTrue(Student.objects.filter(
                        pk=self.user1.id,
                        labGroup=labGroup).exists())
                    labGroup = LabGroup.objects.get(pk=labGroupId)
                    counter += 1
                    self.assertEqual(labGroup.counter, counter)
                else:
                    print(theoryGroup.groupName, "-->",
                          labGroup.groupName, ", Invalid")
                    self.assertFalse(Student.objects.filter(
                        pk=self.user1.id,
                        labGroup=labGroup).exists())
                    labGroup = LabGroup(pk=labGroupId)
                    self.assertEqual(labGroup.counter, counter)

    def test_43_select_group_pair_user2_request(self):
        """Select group for pairs"""
        # login
        self.loginTestUser(self.client2, self.user2)
        # set all theory groups
        tgQS = TheoryGroup.objects.all()
        self.user1.theoryGroup = tgQS.first()
        self.user1.save()
        # set othercostraint.selectGroupStart to now
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now
        o.save()
        # pick valid groups
        # for each theory group
        p = Pair(student1=self.user1, student2=self.user2, validated=True)
        p.save()
        for theoryGroup in tgQS:
            print(theoryGroup.groupName)
            # user2 group is irrelevant
            self.user2.theoryGroup = theoryGroup
            self.user2.save()
            # connect to create group page as user2
            response = self.client2.get(reverse(GROUP_SERVICE), follow=True)
            # check labgroups offered are right
            gcQS = GroupConstraints.objects.filter(theoryGroup=theoryGroup)
            for groupConstraint in gcQS:
                print("    ", groupConstraint.labGroup.groupName)
                # print(groupConstraint.labGroup.groupName)
                # print(self.decode(response.content))
                m = re.search(groupConstraint.labGroup.groupName,
                              self.decode(response.content))
                self.assertTrue(m, "%s labgroup not found in response" %
                                groupConstraint.labGroup.groupName)
        # try to create all groups with all possible combination
        # Theory group, labgroup. some should be invalid
        # use html page instead of function to select groups
        tgQS = TheoryGroup.objects.all()
        lgQS = LabGroup.objects.all()

        for theoryGroup in tgQS:
            for labGroup in lgQS:
                self.user2.theoryGroup = theoryGroup
                # reset labgroup
                self.user2.labGroup = None
                self.user2.save()
                self.user1.labGroup = None
                self.user1.save()
                labGroupId = labGroup.id
                labGroupTmp0 = LabGroup.objects.get(pk=labGroupId)
                counter = labGroupTmp0.counter
                data = {GROUP_FORM_LABEL: labGroupId}
                self.client2.post(reverse(GROUP_SERVICE),
                                  data=data,
                                  follow=True)
                valid = GroupConstraints.objects.filter(
                    theoryGroup=theoryGroup,
                    labGroup=labGroup).exists()
                if valid:
                    self.assertTrue(Student.objects.filter(
                        pk=self.user1.id,
                        labGroup=labGroup).exists(),
                                    "user2 has not labGroup assigned")
                    self.assertTrue(Student.objects.filter(
                        pk=self.user2.id,
                        labGroup=labGroup).exists(),
                                    "user2 has not labGroup assigned")
                    labGroupTmp1 = LabGroup.objects.get(pk=labGroupId)
                    self.assertEqual(labGroupTmp1.counter, counter+2)
                else:
                    self.assertFalse(Student.objects.filter(
                        pk=self.user1.id,
                        labGroup=labGroup).exists())
                    self.assertFalse(Student.objects.filter(
                        pk=self.user2.id,
                        labGroup=labGroup).exists())
                    labGroupTmp2 = LabGroup.objects.get(pk=labGroupId)
                    self.assertEqual(labGroupTmp2.counter, counter)

    def test_44_oversubscrition(self):
        "disable labgroup when full"
        # login
        self.loginTestUser(self.client1, self.user1)
        # assign theory group to user
        theoryGroup = TheoryGroup.objects.all().first()
        self.user1.theoryGroup = theoryGroup
        self.user1.save()
        # set othercostraint.selectGroupStart to now
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now
        o.save()
        # assign maximum number of students and count to labGroup
        labGroup = GroupConstraints.objects.filter(theoryGroup=theoryGroup).first().labGroup
        labGroup.counter = 2
        labGroup.maxNumberStudents = 2
        labGroup.save()
        # try to reserve
        labGroupId = labGroup.id
        data = {GROUP_FORM_LABEL: labGroupId}
        self.client1.post(reverse(GROUP_SERVICE),
                          data=data,
                          follow=True)
        # refresh user
        user = Student.objects.get(pk = self.user1.id)
        self.assertIsNone(user.labGroup)
        self.assertEqual(labGroup.counter, 2)
        # increase maxNumberStudents
        labGroup.counter = 2
        labGroup.maxNumberStudents = 3
        labGroup.save()
        # try to reserve
        labGroupId = labGroup.id
        data = {GROUP_FORM_LABEL: labGroupId}
        self.client1.post(reverse(GROUP_SERVICE),
                          data=data,
                          follow=True)
        # refresh user and labGroup
        user = Student.objects.get(pk=self.user1.id)
        labGroup = LabGroup.objects.get(pk=labGroup.id)
        self.assertEqual(user.labGroup.id, labGroup.id)
        self.assertEqual(labGroup.counter, 3)

