import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labassign.settings")
django.setup()

from core.models import (Student, Pair,
                         OtherConstraints)

from datetime import datetime, timedelta
from django.utils.timezone import make_aware, make_naive

# Check student with ID = 1000
user_1000, created = Student.objects.get_or_create(
                                        id=1000,
                                        defaults={
                                            'username': 'User1000',
                                            'first_name': 'User',
                                            'last_name': '1000',
                                            'labGroup': None,
                                            'theoryGroup': None,
                                            'gradeTheoryLastYear': None,
                                            'gradeLabLastYear': None,
                                            'convalidationGranted': None,
                                                   })
if (created):
    user_1000.save()

# Check student with ID = 1001
user_1001, created = Student.objects.get_or_create(
                                            id=1001,
                                            defaults={
                                                'username': 'User1001',
                                                'first_name': 'User',
                                                'last_name': '1001',
                                                'labGroup': None,
                                                'theoryGroup': None,
                                                'gradeTheoryLastYear': None,
                                                'gradeLabLastYear': None,
                                                'convalidationGranted': None,
                                                   })
if (created):
    user_1001.save()

# Create pair
pair, created = Pair.objects.get_or_create(id=1000,
                                           student1=user_1000,
                                           defaults={
                                               'student2': user_1001,
                                               'validated': False,
                                               'studentBreakRequest': None})

if created is not False:
    pair.student2 = user_1001
    pair.validated = False
    pair.studentBreakRequest = None

pair.save()

# Search pairs with user_1000 as student1
pairs = Pair.objects.filter(student1=user_1000)
print('Result of query where student1 is user_1000', pairs)

# Set the validation to true
for pair in pairs:
    pair.validated = True
    pair.save()

# Set the date to select the group
date = make_aware(datetime.now() + timedelta(days=1))

oc = OtherConstraints.objects.create(selectGroupStartDate=date,
                                     minGradeTheoryConv=0,
                                     minGradeLabConv=0)

# First object fo the type OtherConstraints and compares the date with today.
date = make_naive(OtherConstraints.objects.all()[0].selectGroupStartDate)
print('\nOtherConstraints ', end='')
if date < datetime.now():
    print('is in the past.')
elif date > datetime.now():
    print('it is in the future.')
else:
    print('is in the present.')
