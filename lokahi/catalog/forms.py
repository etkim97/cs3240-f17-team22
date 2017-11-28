from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import User
import datetime #for checking renewal date range.

class signUp(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    company = forms.CharField(label="Company", required=False)
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="E-mail")
    OPTIONS = (
        ('Investor',"Investor"),
        ('Company',"Company"),
        )
    user_type = forms.ChoiceField(choices=OPTIONS)
    password = forms.CharField(label="Password")


class CreateReportForm(forms.Form):
    report_name = forms.CharField(label="Report Name")
    company_name = forms.CharField()
    company_phone = forms.CharField()
    company_location = forms.CharField()
    company_country = forms.CharField()
    company_sector = forms.CharField()
    company_industry = forms.CharField()
    current_projects = forms.CharField()
    info = forms.CharField()
    filename = forms.FileField(label="Select a file", widget=forms.ClearableFileInput(attrs={'multiple': True}))
    OPTIONS = (
        ('Private',"Private"),
        ('Public',"Public"),
        )
    privacy_setting = forms.ChoiceField(choices=OPTIONS)
    owner = forms.CharField(label = "Owner (enter your username)")


class EditReportForm(forms.Form):
    company_name = forms.CharField()
    company_phone = forms.CharField()
    company_location = forms.CharField()
    company_country = forms.CharField()
    company_sector = forms.CharField()
    company_industry = forms.CharField()
    current_projects = forms.CharField()
    info = forms.CharField()

class CreateMessageForm(forms.Form):
    recipient = forms.CharField()
    message_body = forms.CharField()
    privacy = forms.BooleanField(initial=True)

class CreateGroupForm(forms.Form):
    #users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    users = forms.CharField()
    group_name = forms.CharField()
    group_reports = forms.CharField() 

class user_privileges(forms.Form):
    CHOICES = (
        ('False', "False"),
        ('True', "True"),
        )
    may_suspend_users = forms.ChoiceField(CHOICES)
    may_delete_reports = forms.ChoiceField(CHOICES)
    may_delete_users = forms.ChoiceField(CHOICES)
