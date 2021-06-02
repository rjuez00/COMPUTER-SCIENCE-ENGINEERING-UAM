# code created by R.Juez and J.M. Freire
import re
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from core.models import (Student, OtherConstraints,
                         Pair, TheoryGroup, GroupConstraints,
                         LabGroup, Teacher)


# PLease do not modify anything below this line
###################

# TODO: Student class inherits from User
# class Student(User):

FIRST_STUDENT_ID = 1000

GROUPNAME1 = '140'
THEORY_GROUP_ID = 1
HOME_THEORY_SERVICE = 'theory'
HOME_LAB_SERVICE = 'lab'
LOGIN_SERVICE = 'login'
WRONG_LOGIN_SERVICE = 'wronglogin'
CONVALIDATION_SERVICE = 'Convalidation'
GROUP_SERVICE = "applygroup"
GROUP_FULL = 'groupfull'
SERVICE_DEF = {
    HOME_THEORY_SERVICE: {
        "title": 'Home',
        "pattern": r"140"
    },
    HOME_LAB_SERVICE: {
        "title": 'Home',
        "pattern": r"1391"
    },
    LOGIN_SERVICE: {
        "title": 'Login',
        "pattern": r"Please login|Por favor autentiquese"
    },
    WRONG_LOGIN_SERVICE: {
        "title": 'Login',
        "pattern": r"Wrong credentials"
    },
    CONVALIDATION_SERVICE: {
        "title": 'Convalidation',
        "pattern": r"You have validated pairs, break them to convalidate"
    },
    GROUP_SERVICE: {
        "title": 'Apply Group',
        "pattern": r"1391"
    },
    GROUP_FULL: {
        "title": 'Apply Group',
        "pattern": r"fit in this lab group."
    },
}


class AdditionalTest(TestCase):
    def setUp(self):
        """
        Initializes all the models we are going to use in this test module.
        :author: Rodrigo Juez
        """
        self.paramsUser1 = {"username": "testUser_1",
                            "password": "pass1",
                            "first_name": "user1",
                            "last_name": "name1",
                            "id": FIRST_STUDENT_ID}

        self.wrongParamsUser1 = {"username": "testUser_1",
                                 "password": "password?",
                                 "first_name": "user1",
                                 "last_name": "name1",
                                 "id": FIRST_STUDENT_ID}

        self.paramsUser2 = {"username": "testUser_2",
                            "password": "pass2",
                            "first_name": "user2",
                            "last_name": "name2",
                            "id": FIRST_STUDENT_ID + 1}

        self.paramsUser3 = {"username": "testUser_3",
                            "password": "pass3",
                            "first_name": "user3",
                            "last_name": "name3",
                            "id": FIRST_STUDENT_ID + 2}

        self.paramsUser4 = {"username": "testUser_4",
                            "password": "pass4",
                            "first_name": "user4",
                            "last_name": "name4",
                            "id": FIRST_STUDENT_ID + 3}

        self.paramsUser5 = {"username": "testUser_5",
                            "password": "pass5",
                            "first_name": "user5",
                            "last_name": "name5",
                            "id": FIRST_STUDENT_ID + 4}

        self.theoryGroup1 = {"groupName": GROUPNAME1,
                             "id": THEORY_GROUP_ID}

        self.theorygroup1 = TheoryGroup.objects.create(
            id=self.theoryGroup1['id'],
            groupName=self.theoryGroup1['groupName'])

        self.teacher1 = Teacher.objects.create(id=1,
                                               first_name='Test',
                                               last_name='Teacher')
        self.labgroup1 = LabGroup.objects.create(
            id=1,
            groupName='1391',
            maxNumberStudents=20,
            counter=1,
            schedule="schedule",
            language="language",
            teacher=self.teacher1)

        self.labgroup2 = LabGroup.objects.create(
            id=2,
            groupName='1392',
            maxNumberStudents=1,
            counter=1,
            schedule="schedule",
            language="language",
            teacher=self.teacher1)

        self.groupconstrains = GroupConstraints.objects.create(
            id=1, theoryGroup=self.theorygroup1, labGroup=self.labgroup1
        )

        self.groupconstrains = GroupConstraints.objects.create(
            id=2, theoryGroup=self.theorygroup1, labGroup=self.labgroup2
        )

        self.user1 = Student.objects.create_user(
            id=self.paramsUser1["id"],
            username=self.paramsUser1["username"],
            password=self.paramsUser1["password"],
            first_name=self.paramsUser1["first_name"],
            last_name=self.paramsUser1["last_name"],
            theoryGroup=self.theorygroup1,
            gradeTheoryLastYear=10,
            gradeLabLastYear=10)

        self.user2 = Student.objects.create_user(
            id=self.paramsUser2["id"],
            username=self.paramsUser2["username"],
            password=self.paramsUser2["password"],
            first_name=self.paramsUser2["first_name"],
            last_name=self.paramsUser2["last_name"],
            theoryGroup=self.theorygroup1,
        )

        self.user3 = Student.objects.create_user(
            id=self.paramsUser3["id"],
            username=self.paramsUser3["username"],
            password=self.paramsUser3["password"],
            first_name=self.paramsUser3["first_name"],
            last_name=self.paramsUser3["last_name"],
            theoryGroup=self.theorygroup1,
        )

        self.user4 = Student.objects.create_user(
            id=self.paramsUser4["id"],
            username=self.paramsUser4["username"],
            password=self.paramsUser4["password"],
            first_name=self.paramsUser4["first_name"],
            last_name=self.paramsUser4["last_name"],
            theoryGroup=self.theorygroup1,
        )

        self.user5 = Student.objects.create_user(
            id=self.paramsUser5["id"],
            username=self.paramsUser5["username"],
            password=self.paramsUser5["password"],
            first_name=self.paramsUser5["first_name"],
            last_name=self.paramsUser5["last_name"],
            theoryGroup=self.theorygroup1,
            labGroup=self.labgroup1

        )

        self.alumnodb = Student.objects.create_user(
            id=1,
            username='alumnodb',
            password='alumnodb',
        )

        self.pair1 = Pair.objects.create(id=1,
                                         student1=self.user1,
                                         student2=self.user2,
                                         validated=True,
                                         studentBreakRequest=None)
        self.pair2 = Pair.objects.create(id=2,
                                         student1=self.user3,
                                         student2=self.user4,
                                         validated=True,
                                         studentBreakRequest=None)
        self.otherConstraints = OtherConstraints.objects.create(
            selectGroupStartDate=make_aware(datetime.now()),
            minGradeTheoryConv=7,
            minGradeLabConv=7)

    @classmethod
    def decode(cls, txt):
        """
        Decodes the text encoded in utf-8.
        :author: Rodrigo Juez
        :param txt: the string we want to decode
        :return: the decoded string
        """
        return txt.decode("utf-8")

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
        if(m is None):
            print(response.content)

        self.assertTrue(m)
        return m

    def tearDown(self):
        # This class was made in case we need it in the future.
        pass

    @classmethod
    def login_user(cls, client, params):
        """
        Logs the user in, for the next functions.
        :author: Rodrigo Juez
        :param client: the client we use to log in
        :param params: the data we provide to the page to get logged in
        """
        client.post(reverse(LOGIN_SERVICE),
                    params,
                    follow=True)

    def test_homepage_with_theorygroup_loads(self, ):
        """
        Tests if the home page works with the theory groups.
        :author: Rodrigo Juez
        """
        self.login_user(self.client, self.paramsUser1)
        response = self.client.get(reverse('index'), follow=True)
        self.assertIsNotNone(response)
        self.validate_response(HOME_THEORY_SERVICE, response)

    def test_applygroup_student2_user2(self, ):
        """
        Checks if gives error when user1 applies
        for group and user2 is part of the pair.

        :author: Rodrigo Juez
        """
        self.login_user(self.client, self.paramsUser1)
        response = self.client.post(reverse(GROUP_SERVICE),
                                    data={'group': self.labgroup1.id},
                                    follow=True)
        self.validate_response(GROUP_SERVICE, response)

    def test_applygroup_student2_user1(self, ):
        """
        Checks if gives error when user2 applies
        for group and user1 is part of the pair.

        :author: Rodrigo Juez
        """
        self.login_user(self.client, self.paramsUser4)
        response = self.client.post(reverse(GROUP_SERVICE),
                                    data={'group': self.labgroup1.id},
                                    follow=True)
        self.validate_response(GROUP_SERVICE, response)

    def test_homepage_with_labgroup_loads(self, ):
        """
        Tests if the home page works with the labgroups.
        :author: Rodrigo Juez
        """
        self.login_user(self.client, self.paramsUser5)
        response = self.client.get(reverse('index'), follow=True)
        self.assertIsNotNone(response)
        self.validate_response(HOME_LAB_SERVICE, response)

    def test_convalidate_with_validated_pairs(self, ):
        """
        Tests if the user can covalidate the
        subject once they have a validated pair.

        :author: Rodrigo Juez
        """
        self.login_user(self.client, self.paramsUser1)
        response = self.client.get(reverse('convalidation'), follow=True)
        self.assertIsNotNone(response)
        self.validate_response(CONVALIDATION_SERVICE, response)

    def test_wrongLogin(self):
        """
        Tests if the user can log in with invalid credentials.
        :author: Jose Manuel Freire
        """
        response = self.client.post(reverse(LOGIN_SERVICE),
                                    self.wrongParamsUser1,
                                    follow=True)
        self.validate_response(WRONG_LOGIN_SERVICE, response)

    def test_labgroup_too_small(self):
        """
        Tests if a student can join a labgroup where there's no space for them.
        :author: Jose Manuel Freire
        """
        self.login_user(self.client, self.paramsUser1)
        response = self.client.post(reverse(GROUP_SERVICE),
                                    data={'group': self.labgroup2.id},
                                    follow=True)
        self.validate_response(GROUP_FULL, response)
