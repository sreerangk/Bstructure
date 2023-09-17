from django import forms
from .models import Employee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'report_to', 'position_name']
        
        

# class RegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2')