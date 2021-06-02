import pickle

from django.test import TestCase
from django.test import Client
from os.path import join

from core.models import (Teacher, LabGroup, TheoryGroup,
                         GroupConstraints, Student, Pair,
                         OtherConstraints)
from core.management.commands.populate import Command
###################
# You may modify the following variables
from labassign.settings import BASE_DIR
pathToProject = BASE_DIR
# PLease do not modify anything below this line
###################


class ModelTests(TestCase):
    """Test that populate  has been saved data properly
       require files XXXX.pkl stored in the same directory that manage.py"""
    def setUp(self):
        self.client = Client()
        # load Command class from populate
        c = Command()
        # execute populate
        c.handle(model='all', studentinfo='19-edat_psi.csv',
                 studentinfolastyear='19-edat_2_psi.csv')

    # TODO: ordering attribute need to be defined in meta
    # so the order in the query sets is always the same
    def iterate(self, _class, pklFileName, compareAtrbList):
        if _class == Student:
            dataBaseModelQS = Student.objects.filter(id__gt=1)
        else:
            dataBaseModelQS = _class.objects.all()
        pklFileName = join(pathToProject, pklFileName)
        modelQS = pickle.load(open(pklFileName, "rb"))
        self.assertEqual(len(dataBaseModelQS), len(modelQS),
                         "Error: wrong number of %s" % str(_class))
        counter=1
        for t1, t2 in zip(dataBaseModelQS, modelQS):
            print(counter, t1,t2)
            for attrb in compareAtrbList:
                self.assertEqual(getattr(t1, attrb), getattr(t2, attrb),
                                 "Error: different %s" % attrb)
            # check __str__ functions are defined
            if isinstance(t1, Teacher) or isinstance(t1, Student):
                self.assertFalse(str(t1).find(t1.first_name)==-1)
            if isinstance(t1, LabGroup) or isinstance(t1, TheoryGroup):
                self.assertFalse(str(t1).find(t1.groupName)==-1)
            if isinstance(t1, GroupConstraints):
                self.assertFalse(str(t1).find(t1.theoryGroup.groupName) == -1)
                self.assertFalse(str(t1).find(t1.labGroup.groupName) == -1)
            if isinstance(t1, Pair):
                self.assertFalse(str(t1).find(t1.student1.first_name) == -1)
                self.assertFalse(str(t1).find(t1.student2.first_name) == -1)
            if isinstance(t1, OtherConstraints):
                self.assertFalse(
                    str(t1).find("%.1f" % t1.minGradeLabConv) == -1)
                self.assertFalse(
                    str(t1).find("%.1f" % t1.minGradeTheoryConv) == -1)
            counter += 1

    def test_models(self):
        "Test that all data are saved in database!"
        print("Testing Teachers:")
        self.iterate(Teacher, "teacher.pkl",
                     ['first_name', 'last_name'])
        print("Testing Labgroup:")
        self.iterate(LabGroup, "labgroup.pkl",
                     ['groupName', 'teacher', 'schedule', 'language'])
        print("Testing TheoryGroup:")
        self.iterate(TheoryGroup, "theorygroup.pkl",
                     ['groupName', 'language'])
        print("Testing GroupConstraints:")
        self.iterate(GroupConstraints, "groupconstraints.pkl",
                     ['theoryGroup', 'labGroup'])
        print("Testing Student:")
        self.iterate(Student, "student.pkl",
                     ['labGroup', 'theoryGroup', 'gradeTheoryLastYear',
                      'gradeLabLastYear'])#, 'convalidationGranted'])
        print("Testing Pair:")
        self.iterate(Pair, "pair.pkl",
                     ['student1', 'student2', 'validated'])
        print("Testing OtherConstraints:")
        self.iterate(OtherConstraints, "otherconstraints.pkl",
                     [#'selectGroupStartDate',
                      'minGradeTheoryConv', 'minGradeLabConv'])
