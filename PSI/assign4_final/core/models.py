from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Upper


class Teacher(models.Model):
    """
    Class with all the information of a teacher
    :author: Rodrigo Juez
    :param first_name: the first name of the teacher
    :param last_name: the surname of the teacher
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        ordering = [Upper('last_name'), 'first_name']

    def __str__(self):
        """
        Creates the string for a teacher.
        :return: the string
        """
        string = "\n\tName: " + self.first_name + " " + self.last_name
        return string


class TheoryGroup(models.Model):
    """
    Class with all the information of a theory group
    :author: Rodrigo Juez
    :param groupName: the name of the group
    :param language: the language of the classes
    """
    groupName = models.CharField(max_length=30)
    language = models.CharField(max_length=30)

    def __str__(self):
        """
        Creates the string for a theory group.
        :return: the string
        """
        string = "\n\tGroup Name: " + self.groupName
        string += "\n\tlanguage: " + self.language
        return string

    class Meta:
        ordering = ['groupName']


class LabGroup(models.Model):
    """
    Class with all the information of a labgroup
    :author: Rodrigo Juez
    :param teacher: the teacher of the group
    :param groupName: the name of the group
    :param language: the language of the classes
    :param schedule: the hours of the group
    :param maxNumberStudents: the number of maximum students of the group
    :param counter: the current number of students
    """
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    groupName = models.CharField(max_length=30)
    language = models.CharField(max_length=30)
    schedule = models.CharField(max_length=30)
    maxNumberStudents = models.IntegerField()
    counter = models.IntegerField(default=0)

    def __str__(self):
        """
        Creates the string for a labgroup.
        :return: the string
        """
        string = self.groupName
        string += " (" + str(self.counter) + "/\
                  " + str(self.maxNumberStudents) + ")"
        return string

    class Meta:
        ordering = ['groupName']


# Create your models here.
class Student(User):
    """
    Class with all the information of a student
    :author: Jose Manuel Freire
    :param labGroup: the labgroup of the student
    :param theoryGroup: the theory group of the student
    :param gradeLabLastYear: the grade the student got
                             last year in the practices
    :param gradeTheoryLastYear: the grade the student got
                                last year in the theory classes
    :param convalidationGranted: wether they have to do the practices or not
    """
    labGroup = models.ForeignKey(LabGroup, on_delete=models.PROTECT, null=True)
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.PROTECT,
                                    null=True)
    gradeTheoryLastYear = models.FloatField(null=True)
    gradeLabLastYear = models.FloatField(null=True)
    convalidationGranted = models.BooleanField(null=True)

    class Meta:
        ordering = [Upper('last_name'), 'first_name']

    def __str__(self):
        """
        Creates the string for a student.
        :return: the string
        """
        return (self.last_name + ', ' + self.first_name)


class Pair(models.Model):
    """
    Class with all the information of a pair
    :author: Jose Manuel Freire
    :param student1: the first student of the pair
    :param student2: the second student of the pair
    :param validated: wether the pair is validated
    :param studentBreakRequest: wether a student wants to leave the pair
    """
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE,
                                 related_name="student1")
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE,
                                 related_name="student2")
    validated = models.BooleanField(null=True)
    studentBreakRequest = models.ForeignKey(Student, on_delete=models.CASCADE,
                                            null=True)

    class Meta:
        ordering = ['student1__id', 'student2__id']

    def __str__(self):
        """
        Creates the string for a pair.
        :return: the string
        """
        string = "\n\tStudent 1: " + str(self.student1)
        string += "\n\tStudent 2: " + str(self.student2)
        string += "\n\tValidated: " + str(self.validated)
        return string


class GroupConstraints(models.Model):
    """
    Class with all the information to attach a lab group to a theory group
    :author: Rodrigo Juez
    :param theoryGroup: the theory group
    :param labGroup: the labgroup
    """
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)

    class Meta:
        ordering = ['labGroup', 'theoryGroup']

    def __str__(self):
        """
        Creates the string for a group constraints.
        :return: the string
        """
        string = "\n\tLab group " + str(self.labGroup.groupName)
        string += "belongs to theory group " + str(self.theoryGroup.groupName)
        return string


class OtherConstraints(models.Model):
    """
    Class with other information for the lab assignment
    :author: Jose Manuel Freire
    :param selectGroupStartDate: the date the pairs will
                                 be able to start picking groups
    :param minGradeTheoryConv: the mimnimum grade in theory
                               to convalidate the practices
    :param minGradeLabConv: the mimnimum grade in practices
                            to convalidate the practices
    """
    selectGroupStartDate = models.DateTimeField()
    minGradeTheoryConv = models.FloatField()
    minGradeLabConv = models.FloatField()

    def __str__(self):
        """
        Creates the string for other constraints.
        :return: the string
        """
        return ('Start Date: ' + str(self.selectGroupStartDate) + '\n' +
                'Min Grade Theory: ' + str(self.minGradeTheoryConv) + '\n' +
                'Min Grade Lab: ' + str(self.minGradeLabConv))
