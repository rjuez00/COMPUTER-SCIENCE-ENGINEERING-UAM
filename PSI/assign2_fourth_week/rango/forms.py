from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile

max_length_url = 200


class CategoryForm(forms.ModelForm):

    name = forms.CharField(
        max_length=Category._meta.get_field('name').max_length,
        help_text='Please enter the category name')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:

        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=Page._meta.get_field('title').max_length,
        help_text="Please enter the title of the page.")

    url = forms.URLField(max_length=max_length_url,
                         help_text="Please enter the URL of the page.")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not (url.startswith('http://')
                        or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        exclude = ('category', )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
