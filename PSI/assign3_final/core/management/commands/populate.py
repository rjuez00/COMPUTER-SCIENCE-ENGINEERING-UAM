# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate


import csv
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from django.contrib.auth import hashers
from core.models import (OtherConstraints, Pair, Student,
                         GroupConstraints, TheoryGroup,
                         LabGroup, Teacher)


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
#
# Teachers, groups and constraints
# will be hardcoded in this file.
# Students will be read from a csv file
# last year grade will be obtained from another csv file
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate database
           """

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help="""
        model to  update:
        all -> all models
        teacher
        labgroup
        theorygroup
        groupconstraints
        otherconstrains
        student (require csv file)
        studentgrade (require different csv file,
        update only existing students)
        pair
        """)
        parser.add_argument('studentinfo', type=str, help="""CSV file with student information
        header= NIE, DNI, Apellidos, Nombre, Teoría
        if NIE or DNI == 0 skip this entry and print a warning""")
        parser.add_argument('studentinfolastyear', type=str, help="""CSV file with student information
        header= NIE,DNI,Apellidos,Nombre,Teoría, grade lab, grade the
        if NIE or DNI == 0 skip this entry and print a warning""")

    # handle is another compulsory name, do not change it"
    def handle(self, *args, **kwargs):
        model = kwargs['model']
        csvStudentFile = kwargs['studentinfo']
        csvStudentFileGrades = kwargs['studentinfolastyear']
        # clean database
        if model == 'all':
            self.cleanDataBase()
        if model == 'teacher' or model == 'all':
            self.teacher()
        if model == 'labgroup' or model == 'all':
            self.labgroup()
        if model == 'theorygroup' or model == 'all':
            self.theorygroup()
        if model == 'groupconstraints' or model == 'all':
            self.groupconstraints()
        if model == 'otherconstrains' or model == 'all':
            self.otherconstrains()
        if model == 'student' or model == 'all':
            self.student(csvStudentFile)
        if model == 'studentgrade' or model == 'all':
            self.studentgrade(csvStudentFileGrades)
        if model == 'pair' or model == 'all':
            self.pair()

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        # remove pass and ADD CODE HERE
        Student.objects.exclude(username='alumnodb').delete()
        OtherConstraints.objects.all().delete()
        Pair.objects.all().delete()
        GroupConstraints.objects.all().delete()
        TheoryGroup.objects.all().delete()
        LabGroup.objects.all().delete()
        Teacher.objects.all().delete()

    def create_teacher(self, idteacher, first_name, last_name):
        """
        The constructor for the teacher.
        :author: Rodrigo Juez
        :param idteacher: the id of the new teacher
        :param first_name: the first name of the new teacher
        :param last_name: the surname of the new teacher
        :return: the new teacher
        """
        c = Teacher.objects.get_or_create(id=idteacher,
                                          first_name=first_name,
                                          last_name=last_name)[0]

        c.save()
        return c

    def teacher(self):
        """
        If fills the database with teachers.
        """
        teacherD = {}
        teacherD[1] = {'id': 1,  # 1261, L 18:00, 1271 X 18-20
                       'first_name': 'No',
                       'last_name': 'Asignado1', }
        teacherD[2] = {'id': 2,  # 1262 X 18-20, 1263/1273 V 17-19
                       'first_name': 'No',
                       'last_name': 'Asignado4', }
        teacherD[3] = {'id': 3,  # 1272 V 17-19, 1291 L 18-20
                       'first_name': 'Julia',
                       'last_name': 'Diaz Garcia', }
        teacherD[4] = {'id': 4,  # 1292/1251V 17:00
                       'first_name': 'Alvaro',
                       'last_name': 'del Val Latorre', }
        teacherD[5] = {'id': 5,  # 1201 X 18:00
                       'first_name': 'Roberto',
                       'last_name': 'Marabini Ruiz', }
        for key, value in teacherD.items():
            self.create_teacher(key, value['first_name'], value['last_name'])

    def create_labgroup(self, idlabgroup, teacher, groupName,
                        language, schedule,
                        maxNumberStudentso, counter):
        """
        The constructor for the labgroup.
        :author: Rodrigo Juez
        :param idlabgroup: the id of the new labgroup
        :param teacher: the teacher of the new labgroup
        :param groupName: the group name of the new labgroup
        :param language: the language of the new labgroup
        :param schedule: the schedule of the new labgroup
        :param maxNumberStudentso: the maximum number of
                                   students of the new labgroup
        :param counter: the number of students already in the new labgroup
        :return: the new labgroup
        """
        labgroup = LabGroup.objects.create(
            id=idlabgroup,
            groupName=groupName,
            maxNumberStudents=maxNumberStudentso,
            counter=counter,
            schedule=schedule,
            language=language,
            teacher=teacher)
        labgroup.save()
        return labgroup

    def labgroup(self):
        """
        If fills the database with lab groups.
        """

        labgroupD = {}
        maxNumberStudents = 23
        # create dictionary with teacher data
        labgroupD[1261] = {'id': 1261,  # 1261, L 18:00, 1271 X 18-20
                           'groupName': '1261',
                           'teacher': 1,
                           'schedule': 'Lunes/Monday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1262] = {'id': 1262,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 2,
                           'groupName': '1262',
                           'schedule': 'Miércoles/Wednesday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1263] = {'id': 1263,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 2,
                           'groupName': '1263',
                           'schedule': 'Viernes/Friday 17-19',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1271] = {'id': 1271,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 1,
                           'groupName': '1271',
                           'schedule': 'Miércoles/Wednesday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1272] = {'id': 1272,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 3,
                           'groupName': '1272',
                           'schedule': 'Viernes/Friday 17-19',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1291] = {'id': 1291,  # 1261, L 18:00, 1271 X 18-20
                           'teacher': 3,
                           'groupName': '1291',
                           'schedule': 'Lunes/Monday 18-20',
                           'language': 'inglés/English',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1292] = {'id': 1292,
                           'teacher': 4,
                           'groupName': '1292',
                           'schedule': 'Viernes/Friday 17-19',
                           'language': 'inglés/English',
                           'maxNumberStudents': maxNumberStudents}
        labgroupD[1201] = {'id': 1201,
                           'teacher': 5,
                           'groupName': '1201',
                           'schedule': 'Miércoles/Wednesday 18-20',
                           'language': 'español/Spanish',
                           'maxNumberStudents': maxNumberStudents}

        for key, value in labgroupD.items():
            teacherReference = Teacher.objects.get(id=value['teacher'])
            self.create_labgroup(
                key,
                teacherReference,
                value['groupName'],
                value['language'],
                value['schedule'],
                value['maxNumberStudents'],
                0)

    def create_theorygroup(self, idtheory, groupName, language):
        """
        The constructor for the theory group.
        :author: Rodrigo Juez
        :param idtheoryr: the id of the new theory group
        :param groupName: the group name of the new theory group
        :param language: the language of the new theory group
        :return: the new theory group
        """
        theorygroup = TheoryGroup.objects.create(
            id=idtheory, groupName=groupName)
        theorygroup.language = language
        theorygroup.save()
        return theorygroup

    def theorygroup(self):
        """
        If fills the database with theory groups.
        """
        theorygroupD = {}
        theorygroupD[126] = {'id': 126,
                             'groupName': '126',
                             'language': 'español/Spanish', }
        theorygroupD[127] = {'id': 127,  # 127/120
                             'groupName': '127',
                             'language': 'español/Spanish', }
        theorygroupD[129] = {'id': 129,  # 129/125
                             'groupName': '129',
                             'language': 'inglés/English', }
        theorygroupD[120] = {'id': 120,  # 127/120
                             'groupName': '120',
                             'language': 'español/Spanish', }
        theorygroupD[125] = {'id': 125,  # 129/125
                             'groupName': '125',
                             'language': 'inglés/English', }

        for key, value in theorygroupD.items():
            self.create_theorygroup(key, value['groupName'], value['language'])

    def create_groupConstrains(self, idgroupcons, theoryGroup, labGroup):
        """
        The constructor for the group constriants.
        :author: Rodrigo Juez
        :param idgroupcons: the id of the new group constriants
        :param theoryGroup: the theoryGroup of the new group constriants
        :param labGroup: the labGroup of the new group constriants
        :return: the new group constriants
        """
        groupconstrains = GroupConstraints.objects.create(
            id=idgroupcons, theoryGroup=theoryGroup, labGroup=labGroup)

        groupconstrains.save()
        return groupconstrains

    def groupconstraints(self):
        """
        If fills the database with group constraints.
        """
        groupconstraintsD = {}
        groupconstraintsD[1261] = {
            'theoryGroup': 126,
            'labGroup': 1261}  # mañana
        groupconstraintsD[1262] = {
            'theoryGroup': 126,
            'labGroup': 1262}  # mañana
        groupconstraintsD[1263] = {
            'theoryGroup': 126,
            'labGroup': 1263}  # mañana
        # tarde, split ii and doble
        groupconstraintsD[1271] = {
            'theoryGroup': 127,
            'labGroup': 1271}  # tarde - no doble
        groupconstraintsD[1272] = {
            'theoryGroup': 127,
            'labGroup': 1272}  # tarde - no doble
        groupconstraintsD[1201] = {
            'theoryGroup': 120,
            'labGroup': 1201}  # doble - tarde - español - WEds
        # english
        groupconstraintsD[1291] = {
            'theoryGroup': 129,
            'labGroup': 1291}  # inglés - ii - tarde Friday
        groupconstraintsD[1292] = {
            'theoryGroup': 125,
            'labGroup': 1292}  # inglés - doble
        # groupconstraintsD[1202] = {'theoryGroup' : 120, 'labGroup': 1202} #
        # doble - tarde - 2nd group

        for key, value in groupconstraintsD.items():
            theorygroup = None
            theorygroup = TheoryGroup.objects.get(
                groupName=value['theoryGroup'])
            labgroup = LabGroup.objects.get(groupName=value['labGroup'])
            self.create_groupConstrains(key, theorygroup, labgroup)

    def create_pair(self, idpair, student1, student2, validated):
        """
        The constructor for the pair.
        :author: Jose Manuel Freire
        :param idpair: the id of the new pair
        :param student1: the first student of the new pair
        :param student2: the second student of the new pair
        :param validated: wether the new pair is validated or not
        :return: the new pair
        """
        pairvariable = Pair.objects.create(id=idpair,
                                           student1=student1,
                                           student2=student2,
                                           validated=validated,
                                           studentBreakRequest=None)
        pairvariable.save()
        return pairvariable

    def pair(self):
        """
        If fills the database with pairs.
        """
        pairD = {}
        # Mañana
        pairD[1000] = {'student2': 1100, 'validated': False}
        pairD[1001] = {'student2': 1101, 'validated': False}
        pairD[1010] = {'student2': 1110, 'validated': True}
        pairD[1011] = {'student2': 1111, 'validated': True}
        pairD[1012] = {'student2': 1112, 'validated': True}

        for key, value in pairD.items():
            student1Reference = Student.objects.get(id=key)
            student2Reference = Student.objects.get(id=value['student2'])
            self.create_pair(
                key,
                student1Reference,
                student2Reference,
                value['validated'])

    def create_otherconstrains(self, selectGroupStartDate,
                               minGradeTheoryConv, minGradeLabConv):
        """
        The constructor for the other constraints.
        :author: Jose Manuel Freire
        :param selectGroupStartDate: the date from the
                                     students can pick a labgroup
        :param minGradeTheoryConv: the minimum grade in
                                   theory to convalidate practices
        :param minGradeLabConv: the minimum grade in practices
                                to convalidate practices
        :return: the new other constraints
        """
        o = OtherConstraints.objects.get_or_create(
            selectGroupStartDate=make_aware(selectGroupStartDate),
            minGradeTheoryConv=minGradeTheoryConv,
            minGradeLabConv=minGradeLabConv)[0]
        o.save()
        return o

    def otherconstrains(self):
        """create a single object here with staarting dates
        and maximum and minimum convalidation grades"""
        """ Use the following values:
        selectGroupStartDate = now + 1 day,
        minGradeTheoryConv = 3,
        minGradeLabConv = 7
        """
        date = datetime.now()
        date += timedelta(days=1)
        self.create_otherconstrains(date, 3, 7)

    def read_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            lines = [line for line in reader]
        return [dict(zip(lines[0], lines[i])) for i in range(len(lines))][1:]

    def create_student(self, idstudent, first_name, last_name, password,
                       username, labgroup, theorygroup,
                       gradetheorylastyear, gradelablastyear,
                       convalidationgranted):
        """
        The constructor for the student.
        :author: Jose Manuel Freire
        :param idstudent: the id of the new student
        :param first_name: the first name of the new student
        :param last_name: the surname of the new student
        :param password: the password of the new student
        :param username: the username of the new student
        :param labgroup: the lab group of the new student
        :param theorygroup: the theory group of the new student
        :param gradetheorylastyear: the grade of the
                                    new student in theory
                                    last year
        :param gradelablastyear: the grade of the new student
                                 in practices last year
        :param convalidationgranted: wether the new student
                                     has the practices convalidated
        :return: the new student
        """
        o = Student.objects.create(
            id=idstudent,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=hashers.make_password(password),
            labGroup=labgroup,
            theoryGroup=theorygroup,
            gradeTheoryLastYear=gradetheorylastyear,
            gradeLabLastYear=gradelablastyear,
            convalidationGranted=False)

        o.save()
        return o

    def student(self, csvStudentFile):
        """
        If fills the database with students.
        """
        i = 1000
        for student in self.read_csv(csvStudentFile):
            actualtheorygroup = TheoryGroup.objects.get(
                groupName=student['grupo-teoria'])
            actuallabgroup = None

            self.create_student(i,
                                student['Nombre'],
                                student['Apellidos'],
                                student['DNI'],
                                student['NIE'],
                                actuallabgroup,
                                actualtheorygroup,
                                0, 0, False)
            i += 1

    def studentgrade(self, csvStudentFileGrades):
        """
        It fills the grades of the students with their scores last year.
        """
        for student in self.read_csv(csvStudentFileGrades):
            thisstudent = Student.objects.filter(username=student['NIE'])
            if len(thisstudent) > 0:
                thisstudent = thisstudent[0]
                thisstudent.gradeLabLastYear = student['nota-practicas']
                thisstudent.gradeTheoryLastYear = student['nota-teoria']
                thisstudent.save()
