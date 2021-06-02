from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from core.models import Student, Pair
from core.models import OtherConstraints, GroupConstraints
from core.models import LabGroup
from django.utils.timezone import make_naive
from datetime import datetime

# Create your views here.


def home(request):
    """
    Displays the home page
    :author: Rodrigo Juez
    :param request: the request
    :return: the request, the html that has to be displayed and the context
    """

    context_dict = {}
    if request.user.is_authenticated:

        student = Student.objects.get(username=request.user.username)
        if student.theoryGroup:
            context_dict['theoryGroup'] = student.theoryGroup.groupName
        else:
            context_dict['theoryGroup'] = 'none'

        context_dict['convalidated'] = student.convalidationGranted
        pair = Pair.objects.all().filter(
            student1=student) | Pair.objects.all().filter(
            student2=student)
        boom = []
        # this is just in case there is a bug
        # and a student has two pairs but it shouldn't happen
        for result in pair:
            name1 = (result.student1.last_name + ', ' +
                     result.student1.first_name)

            name2 = (result.student2.last_name + ', ' +
                     result.student2.first_name)
            boom.append((name1, name2, result.validated))
        context_dict['pairs'] = boom
        if student.labGroup:
            context_dict['labGroup'] = student.labGroup.groupName
        else:
            context_dict['labGroup'] = None

    return render(request, 'core/home.html', context=context_dict)


@login_required
def convalidation(request):
    """
    Displays the convalidation page
    :author: Rodrigo Juez
    :param request: the request
    :return: the request, the html that has to be displayed and context
    """

    context_dict = {}

    username = request.user.username
    student = Student.objects.get(username=username)
    context_dict['theory'] = student.gradeTheoryLastYear
    context_dict['lab'] = student.gradeLabLastYear
    context_dict['granted'] = student.convalidationGranted
    if student.convalidationGranted:
        return render(request, 'core/convalidation.html', context=context_dict)

    info = OtherConstraints.objects.all()[0]

    if (student.gradeTheoryLastYear >= info.minGradeTheoryConv and
            student.gradeLabLastYear >= info.minGradeLabConv):
        # | Pair.objects.all().filter(student2 = student)
        pairs = Pair.objects.all().filter(student1=student)
        if len(pairs) > 0:
            if len([pair for pair in pairs if pair.validated]) > 0:
                context_dict['alert'] = 'You have validated pairs, ' +\
                                        'break them to convalidate'
            else:
                context_dict['alert'] = 'You have unvalidated pairs,' +\
                                        'delete them to convalidate'

            student.convalidationGranted = False
            student.save()
            return render(
                request,
                'core/convalidation.html',
                context=context_dict)
        else:
            student.convalidationGranted = True
            student.save()
            return redirect(reverse('convalidation'))
    else:
        student.convalidationGranted = False
        student.save()
        context_dict['alert'] = 'Your grades do not satisfy' +\
                                'the requirements to convalidate'
        return render(request, 'core/convalidation.html', context=context_dict)


def user_login(request):
    """
    Displays the login page (if GET) or processes the login request (if POST)
    :author: Rodrigo Juez
    :param request: the request
    :return: the request, the html that has to be displayed
             and context (if GET)
             or the call to load the view of home (if POST)
    """

    context_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('home'))
        else:
            context_dict['alert'] = 'Wrong credentials'

    return render(request, 'core/login.html', context=context_dict)


@login_required
def user_logout(request):
    """
    Processes the logout request
    :author: Rodrigo Juez
    :param request: the request
    :return: the call to load the view of home
    """

    logout(request)
    return redirect(reverse('home'))

# this is not directly called that's why it doesn't need the login_required


def process_applypair_post(request):
    """
    Processes the apply pair request
    :author: Rodrigo Juez
    :param request: the request
    :return: the call to load the view of applypair
    """

    student1 = Student.objects.get(username=request.user.username)
    student2 = Student.objects.get(id=request.POST.get('students'))

    pair = Pair.objects.all().filter(student1=student1)
    # i added this code to avoid the bug in the teacher's page
    # such that if you access to the apply pair cached page
    # and resend the post even though you've already sent it
    if len(pair) > 0:
        return redirect(reverse('applypair'))

    pair = Pair.objects.all().filter(student1=student2, student2=student1)
    if len(pair) == 0:
        pairvariable = Pair.objects.create(student1=student1,
                                           student2=student2,
                                           validated=False,
                                           studentBreakRequest=None)
        pairvariable.save()
    else:
        pair[0].validated = True
        pair[0].save()

    return redirect(reverse('applypair'))


@login_required
def applypair(request):
    """
    Displays the applypair page
    :author: Rodrigo Juez
    :param request: the request
    :return: the request, the html that has to be displayed and context
    """

    if request.method == 'POST':
        return process_applypair_post(request)

    context_dict = {}
    not_valid_students = []
    pair_applied = None
    student = Student.objects.get(username=request.user.username)

    for pair in Pair.objects.all():
        if pair.student1 == student or (
                pair.student2 == student and pair.validated):
            pair_applied = pair
            # if I already applied show me what I applied for
            break  # or if I'm member of a validated pair

        if pair.validated:
            not_valid_students.append(pair.student1)
            not_valid_students.append(pair.student2)

    if pair_applied is not None:
        context_dict['pair_applied'] = (
            pair_applied.student1,
            pair_applied.student2,
            pair_applied.validated)
    else:
        not_valid_students.append(student)

        context_dict['valid_students'] = [
            (item.id,
             item.first_name,
             item.last_name,
             item.username)
            for item
            in Student.objects.all() if item not in not_valid_students]
    return render(request, 'core/applypair.html', context=context_dict)


def process_applygroup_post(request):
    """
    Processes the apply group request
    :author: Rodrigo Juez
    :param request: the request
    :return: the call to load the view of applygroup
    """

    context_dict = {}
    student = Student.objects.get(username=request.user.username)
    group = LabGroup.objects.get(groupName=request.POST.get('group'))

    constraint = GroupConstraints.objects.filter(
        theoryGroup=student.theoryGroup, labGroup=group)
    if len(constraint) == 0:
        context_dict['alert'] = "You are selecting a group that is not allowed"
        return render(request, 'core/applygroup.html', context=context_dict)

    validpair = None
    nstudents = 1
    pairs = Pair.objects.all().filter(
        student1=student) | Pair.objects.all().filter(
        student2=student)

    for pair in pairs:
        if pair.validated:
            validpair = pair
            nstudents = 2
            break

    if (group.counter + nstudents) > group.maxNumberStudents:
        if validpair is not None:
            context_dict['alert'] = "You don't fit in this lab group"
        else:
            context_dict['alert'] = ("You and your" +
                                     "partner don't fit in this lab group")
        return render(request, 'core/applygroup.html', context=context_dict)

    group.counter += nstudents
    group.save()
    student.labGroup = group
    student.save()
    if validpair is not None:
        if validpair.student2 == student:
            student2 = validpair.student1
        else:
            student2 = validpair.student2

        student2.labGroup = group
        student2.save()

    return redirect(reverse('applygroup'))


@login_required
def applygroup(request):
    """
    Displays the apply group page
    :author: Rodrigo Juez
    :param request: the request
    :return: the request, the html that has to be displayed and context
    """

    context_dict = {}
    if make_naive(OtherConstraints.objects.all()[
                  0].selectGroupStartDate) > datetime.now():
        context_dict['startDate'] = OtherConstraints.objects.all()[
            0].selectGroupStartDate
        return render(request, 'core/applygroup.html', context=context_dict)

    if request.method == 'POST':
        return process_applygroup_post(request)

    student = Student.objects.get(username=request.user.username)
    if student.labGroup is not None:
        context_dict['groupName'] = student.labGroup.groupName
    else:  # TODO add free spots
        context_dict['dropdown'] = [
            (constraint.labGroup.groupName,
             constraint.labGroup.counter,
             constraint.labGroup.maxNumberStudents)
            for constraint in GroupConstraints.objects.filter(
                theoryGroup=student.theoryGroup)]

    return render(request, 'core/applygroup.html', context=context_dict)
