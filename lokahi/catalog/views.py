from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.db import models
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime
from .models import User, Report, Message
from .forms import *

def index(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	# num_reports=Report.objects.all().count()
	# num_messages=Message.objects.count()  # The 'all()' is implied by default.

	# Number of visits to this view, as counted in the session variable.
	num_visits=request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits+1

	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'index.html',
		context={'num_visits':num_visits},
	)


def createAccount(request):
	return render(
		request,
		'create_account.html',
		)

def signup(request):
	if request.method == 'POST':
		form = signUp(request.POST)
		if form.is_valid():
			user = User.objects.create_user(form.cleaned_data['username'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.company = form.cleaned_data['company']
			user.password=form.cleaned_data['password']
			user.email = form.cleaned_data['email']
			user.user_type = form.cleaned_data['user_type']
			user.save()
			# print(form.cleaned_data['username'])
			return redirect('/')
	else:
		form = signUp()
	return render(request, 'signup.html', {'form': form})

# =======
#     if request.method == 'POST':
#         form = signUp(request.POST)
#         if form.is_valid():
#            user = User.objects.create_user(form.cleaned_data['username'])
#            # USERNAME_FIELD = form.cleaned_data['username']
#            user.first_name = form.cleaned_data['first_name']
#            user.last_name = form.cleaned_data['last_name']
#            user.company = form.cleaned_data['company']
#            passw = make_password(form.cleaned_data['password'])
#            user.password = passw
#            user.email = form.cleaned_data['email']
#            user.user_type = form.cleaned_data['user_type']
#            user.save()
#            login(request, user)
#            # print(form.cleaned_data['username'])
#            return redirect('/')
#     else:
#         form = signUp()
#     return render(request, 'signup.html', {'form': form})

def log_in(request, template_name="registration/login.html"):
    if request.method == "POST":
        postdata = request.POST.copy()
        username = postdata.get('username', '')
        password = postdata.get('password', '')

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
        except: 
            error = True
    return render(request, template_name, locals())
# >>>>>>> 9cd703112eb5ec1e32c1f054e1c953c18296fe39

class ReportsByUserListView(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view accessible reports to current user.
	"""
	model = Report
	template_name ='catalog/list_reports.html'
	paginate_by = 10


@csrf_exempt
def report_detail(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		context = {
			"report_name": report.report_name,
			"company_name": report.company_name,
			"company_phone": report.company_phone,
			"company_location": report.company_location,
			"company_country": report.company_country,
			"company_sector": report.company_sector,
			"company_industry": report.company_industry,
			"current_projects": report.current_projects,
			"info": report.info,
			"filename": report.filename,
			"privacy_setting": report.privacy_setting,
			"timestamp": report.timestamp,
		}
		return render(request, 'catalog/detailedreport.html', context=context)
	except Exception as e:
		return HttpResponse(e)

@csrf_exempt
def create_report(request):
    if request.method == 'POST':
        form = CreateReportForm(request.POST)
        if form.is_valid():
            report_name = form.cleaned_data['report_name']
            company_name = form.cleaned_data['company_name']
            company_phone = form.cleaned_data['company_phone']
            company_location = form.cleaned_data['company_location']
            company_country = form.cleaned_data['company_country']
            company_sector = form.cleaned_data['company_sector']
            company_industry = form.cleaned_data['company_industry']
            current_projects = form.cleaned_data['current_projects']
            info = form.cleaned_data['info']
            filename = form.cleaned_data['filename']
            privacy_setting = form.cleaned_data['privacy_setting']
            owner = form.cleaned_data['owner']
            try:
                report = Report(
					report_name = report_name,
					company_name = company_name,
					company_phone = company_phone,
					company_location = company_location,
					company_country = company_country,
					company_sector = company_sector,
					company_industry = company_industry,
					current_projects = current_projects,
					info = info,
					filename = filename,
					privacy_setting = privacy_setting,
                    owner = owner,
				)
                report.save()
                return HttpResponse("report saved", report)
            except Exception as e:
                return HttpResponse("exception", False)
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = CreateReportForm()
    return render(request, 'create_report.html', {'form': form})


@csrf_exempt
def delete_report(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		report.delete()
		return HttpResponse("report deleted", True, report)
	except:
		return HttpResponse("report does not exist", False)





#DO SAME FOR MESSAGES HERE
class MessagesByUserListView(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view accessible reports to current user.
	"""
	model = Message
	template_name ='catalog/list_messages.html'
	paginate_by = 10

@csrf_exempt
def message_detail(request, message_id):
    """
    """
    try:
        message = Message.objects.get(pk=message_id)
        context = {
            "recipient": message.recipient,
            "message_body": message.message_body,
            "privacy:": message.isItPrivate
        }
        return render(request, 'catalog/detailedmessage.html', context=context)
    except Exception as e:
        return HttpResponse(e)

@csrf_exempt
def create_message(request):
    if request.method == 'POST':
        form = CreateMessageForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['recipient'])
            #recipient = form.cleaned_data['recipient']
            message_body = form.cleaned_data['message_body']
            privacy = form.cleaned_data['privacy']
            # try:
            #     message = Message(
            #         recipient=user,
            #         message_body=message_body,
            #         privacy=privacy
            #     )
            #     user.save()
            #     message.save()
            #     return HttpResponse("message saved", message)
            #
            # except Exception as e:
            #     return HttpResponse("exception", False)
            message = Message(
                recipient=user,
                message_body=message_body,
                isItPrivate = privacy,
            )
            message.save()
            return HttpResponse("message saved", message)
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = CreateMessageForm()

    return render(request, 'create_message.html', {'form': form})

@csrf_exempt
def delete_message(request, report_id):
    try:
        message = Message.objects.get(pk=report_id)
        message.delete()
        return HttpResponse("message deleted", True, message)
    except:
        return HttpResponse("message does not exist", False)