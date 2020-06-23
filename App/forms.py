"""
Forms.py includes the forms to be used in the application.
"""

from django import forms

from App.models import FileModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import UserProfile

class UserForm(UserCreationForm):
    class Meta():
        fields = ('first_name','last_name','username','email','password1','password2')
        model = User

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email Address'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'

class UserUpdateForm(forms.ModelForm):
    class Meta():
        fields = ('first_name','last_name','username','email')
        model = User

    profile_pic = forms.ImageField(label = 'Profile Photo',required = False)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email Address'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'

    def save(self, commit=True):
        instance = super(UserUpdateForm, self).save()
        all_clean_data = super().clean()
        if all_clean_data['profile_pic']:
            user_profile = get_object_or_404(UserProfile, user = instance)
            print(all_clean_data['profile_pic'])
            user_profile.profile_pic = all_clean_data['profile_pic']
            user_profile.save()


        # instance.course = self.course
        # instance.user = self.user
        # if commit:
        #     instance.save()


class FileForm(forms.ModelForm):
    """
    Creating a form that maps to the model: https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/
    This form is used for the file upload.
    """
    class Meta:
        model = FileModel
        fields = ['file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole

        super(FileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save()
        all_clean_data = super().clean()
        user_profile = get_object_or_404(UserProfile, user = self.user)
        print(instance.userprofile)
        instance.userprofile = user_profile
        print(instance.userprofile)
        # print(user_profile)
        # print(all_clean_data['profile_pic'])
        # user_profile.profile_pic = all_clean_data['profile_pic']
        # user_profile.description = all_clean_data['description']
        instance.save()
