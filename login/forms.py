from django import forms
from .models import User
from django.contrib.admin.widgets import AdminDateWidget


class UserForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=AdminDateWidget)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'address', 'city', 'state',
                  'country', 'mobile', 'avatar', 'password', 'confirm_password']


class PersonalDetailsForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'address', 'city', 'state',
                  'country', 'mobile']
        exclude = ['avatar', 'password', 'confirm_password']
