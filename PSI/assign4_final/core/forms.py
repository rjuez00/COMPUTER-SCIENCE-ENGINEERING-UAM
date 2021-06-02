from core.models import Student, Pair
from core.models import GroupConstraints
from core.models import LabGroup
from django import forms


class LoginForm(forms.Form):
    """
    LoginForm processes the fields, and returns the
    username and password
    :author: Rodrigo Juez
    """
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password',
                               max_length=100,
                               widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        """
        LoginForm processes the fields, doesn't need to check anything
        :author: Rodrigo Juez
        :argument:none
        """
        super(LoginForm, self).__init__(*args, **kwargs)


class PairForm(forms.Form):
    """
    PairForm creates the form to choose a pair,
    creating a list with the available pair members
    and gives the selected option to the caller.
    :author: Jose Manuel Freire
    """
    student = forms.ModelChoiceField(queryset=Student.objects.all())

    def __init__(self, user, *args, **kwargs):
        """
        PairForm checks if the pair members are valid
        :author: Jose Manuel Freire
        :argument: user
        """
        super(PairForm, self).__init__(*args, **kwargs)
        students1 = Pair.objects.all().filter(validated=True).values(
                                                                'student1'
                                                                     )
        students2 = Pair.objects.all().filter(validated=True).values(
                                                                'student2'
                                                                    )

        stList = Student.objects.exclude(id__in=students2).exclude(
            id__in=students1).exclude(id=user.id).exclude(pk=1)

        self.fields['student'].queryset = Student.objects.filter(id__in=stList)


class GroupForm(forms.Form):
    """
    GroupForm only one field which is the group itself
    :author: Rodrigo Juez
    """
    group = forms.ModelChoiceField(queryset=LabGroup.objects.all())

    def __init__(self, user, *args, **kwargs):
        """
        GroupForm uses groupconstrains to check if
        the user can apply for the group or not
        :author: Rodrigo Juez
        :argument: user of the session
        """
        super(GroupForm, self).__init__(*args, **kwargs)
        student = Student.objects.get(username=user)
        groups = GroupConstraints.objects.filter(
                                            theoryGroup=student.theoryGroup
                                                 ).values('labGroup')
        self.fields['group'].queryset = LabGroup.objects.filter(id__in=groups)


class BreakPairForm(forms.Form):
    """
    BreakPairForm is just one field of
    the pair that the user wants to break

    :author: Jose Manuel Freire
    """
    pair = forms.ModelChoiceField(queryset=Pair.objects.all())

    def __init__(self, user, *args, **kwargs):
        """
        BreakPairForm filters the ones that are
        not included in the pairs of the users

        :author: Rodrigo Juez
        :argument: user of the session
        """
        super(BreakPairForm, self).__init__(*args, **kwargs)
        student = Student.objects.get(username=user)
        pairs = (Pair.objects.all().filter(student1=student) |
                 Pair.objects.all().filter(student2=student))
        self.fields['pair'].queryset = Pair.objects.filter(id__in=pairs)
