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
from .models import User, Report, Message, Group, Comment
from .forms import *

def index(request):
	return render(
		request,
		'index.html',
	)


def users(request):
	data = User.objects.all()
	return render(
		request,
		'users.html',
		{'data' : data,},
	)

def signup(request):
    if request.method == 'POST':
        form = signUp(request.POST)
        if form.is_valid():
           user = User.objects.create_user(form.cleaned_data['username'])
           # USERNAME_FIELD = form.cleaned_data['username']
           user.first_name = form.cleaned_data['first_name']
           user.last_name = form.cleaned_data['last_name']
           user.company = form.cleaned_data['company']
           passw = make_password(form.cleaned_data['password'])
           user.password = passw
           user.email = form.cleaned_data['email']
           user.user_type = form.cleaned_data['user_type']
           user.save()
           # user.is_suspended = False
           login(request, user)
           # print(form.cleaned_data['username'])
           return redirect('/')
    else:
        form = signUp()
    return render(request, 'signup.html', {'form': form})

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

def suspend(request, uname):
	try: 
		users = User.objects.all()
		for u in users:
			if uname == u.username:
				if u.is_suspended == False:
					context = {
						"username": u.username,
						"suspended": 'suspended',
					}
					u.is_suspended = True
					u.save()
					return render(request, 'suspended.html', context=context)
				else:
					context = {
						"username": u.username,
						"suspended": 'reactivated',
					}
					u.is_suspended = False
					u.save()
					return render(request, 'suspended.html', context=context)
	except Exception as e:
		return HttpResponse(e)


def search(request):
	template_name = "search.html"
	# try:
	# 	a = request.GET.get('report', )
	# except KeyError:
	# 	a = None
	# if a:
	# 	report_list = Report.objects.filter(
	# 		name__icontains=a,
	# 		report_name=Report.filename,
    #
	# 	)
	# else:
	# 	report_list = Report.objects.filter(owner=request.user)
	# return report_list
	try:
		if request.method == "GET":
			return render(request, template_name)
	except Exception as e:
		return HttpResponse(e)

class search_results(generic.ListView):
	template_name = 'catalog/list_results.html'

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
			"url": report.filename.url,
			"filename":report.filename,
			"privacy_setting": report.privacy_setting,
			"timestamp": report.timestamp,
		}
		return render(request, 'catalog/detailedreport.html', context=context)
	except Exception as e:
		return HttpResponse(e)

from django.core.files.storage import FileSystemStorage

@csrf_exempt
def create_report(request):
    if request.method == 'POST':
        form = CreateReportForm(request.POST, request.FILES)
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
            filename = request.FILES['filename']
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
					filename = request.FILES['filename'],
					privacy_setting = privacy_setting,
                    owner = owner,
				)
                report.save()
                return HttpResponse("report saved", report)
            except Exception as e:
                return HttpResponse("exception", False)
        # else:
        #     return HttpResponse(form.cleaned_data['filename'])
    else:
        form = CreateReportForm()
    return render(request, 'create_report.html', {'form': form})


@csrf_exempt
def edit_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    if request.method == 'POST':
        form = EditReportForm(request.POST)
        if form.is_valid():
            report.company_name = form.cleaned_data['company_name']
            report.company_phone = form.cleaned_data['company_phone']
            report.company_location = form.cleaned_data['company_location']
            report.company_country = form.cleaned_data['company_country']
            report.company_sector = form.cleaned_data['company_sector']
            report.company_industry = form.cleaned_data['company_industry']
            report.current_projects = form.cleaned_data['current_projects']
            report.info = form.cleaned_data['info']
            report.filename = form.cleaned_data['filename']
            report.owner = form.cleaned_data['owner']
            report.save()
            return HttpResponse("report updated", True)
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = EditReportForm()
    return render(request, 'edit_report.html', {'form': form})


@csrf_exempt
def delete_report(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		report.delete()
		return HttpResponse("report deleted", True, report)
	except:
		return HttpResponse("report does not exist", False)


@csrf_exempt
def get_comments(request, report_id):
    try:
        comments = []
        comment_list = Comment.objects.all()
        for comment in comment_list:
            if comment.report == Report.objects.get(pk=report_id):
                comments.append(comment)
        context = {
            "comments": comments,
            "id": comment.report
        }
        return render(request, 'catalog/list_comments.html', context=context)
    except Exception as e:
        return HttpResponse(e)
    





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
            message_body = form.cleaned_data['message_body']
            privacy = form.cleaned_data['privacy']
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
def delete_message(request, message_id):
    try:
        message = Message.objects.get(pk=message_id)
        message.delete()
        return HttpResponse("message deleted", True)
    except:
        return HttpResponse("message does not exist", False)


class GroupsByUserListView(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view accessible groups to current user.
	"""
	model = Group
	template_name ='catalog/list_groups.html'
	paginate_by = 10


@csrf_exempt
def group_detail(request, group_name):
	try:
		groups = Group.objects.all()
		for group in groups: 
			if group.name == group_name:
				context = {
				"name": group.name,
				"users": group.users,
				"reports": group.group_reports,
				}
				return render(request, 'catalog/detailedgroup.html', context=context)
	except Exception as e:
		return HttpResponse(e)


@csrf_exempt
def create_group(request):
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			users = form.cleaned_data['users']
			group_name = form.cleaned_data['group_name']
			group_reports = form.cleaned_data['group_reports']
			group = Group(
				name = group_name,
				users = users,
				group_reports = group_reports,
			)
			group.save()
			return HttpResponse("group saved", group)
		else:
			return HttpResponse(form.errors.as_data())
	else:
		form = CreateGroupForm()

	return render(request, 'create_group.html', {'form': form})


