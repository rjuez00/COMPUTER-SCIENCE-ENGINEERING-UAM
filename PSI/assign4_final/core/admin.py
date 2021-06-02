from django.contrib import admin
from core.models import Teacher, TheoryGroup, LabGroup
from core.models import Student, Pair, GroupConstraints
from core.models import OtherConstraints

admin.site.register(Teacher)
admin.site.register(TheoryGroup)
admin.site.register(LabGroup)
admin.site.register(Student)
admin.site.register(Pair)
admin.site.register(GroupConstraints)
admin.site.register(OtherConstraints)
