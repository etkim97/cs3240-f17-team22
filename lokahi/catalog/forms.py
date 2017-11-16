from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class signUp(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    company = forms.CharField(label="Company", required=False)
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="E-mail")
    OPTIONS = (
        ('a',"Investor"),
        ('b',"Company"),
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
    current_projects =  forms.CharField()
    info = forms.CharField()
    filename = forms.CharField()
    privacy_setting = forms.CharField()

    # class Meta:
    #     model = Report
    #     fields = ["report_name","company_name","company_phone","company_location","company_country","company_sector","company_industry", "current_project", "info"]


class CreateMessageForm(forms.Form):
    recipient = forms.CharField()
    message_body = forms.CharField()
