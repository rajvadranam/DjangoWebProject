"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=26,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
 
class StudentForm(UserCreationForm):
    """User creation (student) form which uses boostrap CSS."""
    Short_ID = forms.CharField(max_length=9,required=True, help_text='should be equal to 9 character length.')
    Student_Full_Name = forms.CharField(max_length=26,required=True, help_text='Includes fiest,Middle,Last with space.')
    Department_ID = forms.CharField(max_length=4,required=True, help_text='CS10/CS50/CS70 etc')
    Degree_type = forms.CharField(max_length=2,required=True, help_text='GR/UG/DO')
    gender = forms.CharField(max_length=2,required=True, help_text='M/F/O')
    email= forms.CharField(max_length=26,required=True, help_text='Your complete email !!')
    address = forms.CharField(max_length=250,required=True, help_text='Your complete mailing address !!')
    libraian=forms.BooleanField(initial=False, required=False,help_text='Your should only check this if you are a librarian !!')

class Meta:
        model = User
        fields = ('Short ID', 'Student Full Name','Department ID','Degree type','gender','email', 'password1', 'password2','address','libraian', )