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
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import DES
from Crypto import Random
from django.core.files import File
from django.utils.encoding import smart_str

import random
import os

import datetime
from .models import User, Report, Message, Group, Comment, File
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

@csrf_exempt
def signup(request):
	if request.method == 'POST':
		form = signUp(request.POST)
		if form.is_valid():
			user = User.objects.create_user(form.cleaned_data['username'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.company = form.cleaned_data['company']
			passw = make_password(form.cleaned_data['password'])
			user.password = passw
			user.email = form.cleaned_data['email']
			user.user_type = form.cleaned_data['user_type']

			random_generator = Random.new().read
			key = RSA.generate(1024, random_generator)
			public_key = key.publickey()
			user.public_key = public_key.exportKey(format='PEM')
			user.save()
			login(request, user)
			context = {
				"private_key": key.exportKey(format='PEM').decode().lstrip('-----BEGIN RSA PRIVATE KEY-----\n').rstrip('\n-----END RSA PRIVATE KEY-----'),
			}
			return render(request, 'private_key.html', context=context)
	else:
		form = signUp()
	return render(request, 'signup.html', {'form': form})


def accept_privileges(request, uname):
	users = User.objects.all()
	for u in users:
		if u.username == uname:
			u.accepted_manager_privileges = True
			u.save()
			return render(request, 'accept_privileges.html')
	return render(request, 'accept_privileges.html')


def privileges(request, uname):
	users = User.objects.all()
	user = User()
	for u in users:
		if u.username == uname:
			user = u
	context = {
		'has_manager_privileges' : user.has_manager_privileges,
		'username' : user.username,
	}
	if request.method == 'POST':
		form = user_privileges(request.POST)
		if form.is_valid():
			if form.cleaned_data['has_manager_privileges'] == 'True':
				user.has_manager_privileges = True
			else:
				user.has_manager_privileges = False
				user.accepted_manager_privileges = False
			user.save()
			return redirect('/')
	else:
		form = user_privileges()
	return render(request, 'privileges.html', {'form':form, 'context':context})

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
	try:
		if request.method == "GET":
			return render(request, template_name)
	except Exception as e:
		return HttpResponse(e)


class search_results(generic.ListView):
	template_name = 'catalog/list_results.html'


class ReportsByUserListView(LoginRequiredMixin,generic.ListView):
	model = Report
	template_name ='catalog/list_reports.html'
	paginate_by = 10


@csrf_exempt
def report_detail(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		files = File.objects.all()
		for_report_files = []
		for f in files:
			if f.report == report_id:
				for_report_files.append(f)
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
			# "url": report.filename.url,
			# "filename":report.filename,
			"privacy_setting": report.privacy_setting,
			"timestamp": report.timestamp,
			"files" : for_report_files,
            'get_comments_url': report.get_comments_url,
            'create_comments_url': report.create_comments_url,
		}
		return render(request, 'catalog/detailedreport.html', context=context)
	except Exception as e:
		return HttpResponse(e)

from django.core.files.storage import FileSystemStorage

@csrf_exempt
def create_report(request):
    if request.method == 'POST':
        form = CreateReportForm(request.POST, request.FILES)
        # files = request.FILES.getlist('filename')
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
            files = request.FILES.getlist('filename')
            privacy_setting = form.cleaned_data['privacy_setting']
            owner = form.cleaned_data['owner']
            if owner != request.user.username:
            	return HttpResponse("inputting your username serves as a digital signature, you may not enter an althernate username. Please go back.")
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
					# filename = request.FILES['filename'],
					privacy_setting = privacy_setting,
					owner = owner,
				)
                report.save()
                for f in files:
                	new_file = File(file = f)
                	new_file.report = report.id
                	new_file.save()
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
    context ={
    	'name' : report.report_name,
    	'current_cname' : report.company_name,
    	'current_phone' : report.company_phone,
    	'current_location' : report.company_location,
    	'current_country' : report.company_country,
    	'current_sector' : report.company_sector,
    	'current_industry' : report.company_industry,
    	'current_projects' : report.current_projects,
    	'current_info' : report.info,
    	'owner' : report.owner,
    	# 'files' : report.filename.url,
    	# 'file_name' : report.filename,
    }
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
            # report.filename = form.cleaned_data['filename']
            report.save()
            return HttpResponse("report updated", True)
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = EditReportForm()
    return render(request, 'edit_report.html', context= {'form': form, 'context':context}, )


@csrf_exempt
def delete_report(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		report.delete()
		return HttpResponse("report deleted", True)
	except:
		return HttpResponse("report does not exist", False)


@csrf_exempt
def get_comments(request, report_id):
    try:
        comments = []
        i_d = ''
        comment_list = Comment.objects.all()
        for comment in comment_list:
            if comment.report == Report.objects.get(pk=report_id):
                comments.append(comment)
                if i_d == '':
                	i_d = comment.report
        context = {
            "comments": comments,
            "id": i_d,
        }
        return render(request, 'catalog/list_comments.html', context=context)
    except Exception as e:
    	return HttpResponse(e)


@csrf_exempt
def create_comment(request, report_id):
	if request.method == 'POST':
		form = CreateCommentForm(request.POST)
		if form.is_valid():
			try:
				report = Report.objects.get(pk=report_id)
			except Exception as e:
				return HttpResponse(e)
			author = User.objects.get(username=form.cleaned_data['author'])
			text = form.cleaned_data['text']
			comment = Comment(
				report=report,
				author=author,
				text=text,
			)
			comment.save()
			return HttpResponse("comment saved", comment)
		else:
			return HttpResponse(form.errors.as_data())
	else:
		form = CreateCommentForm()

	return render(request, 'create_comment.html', {'form': form})



class MessagesByUserListView(LoginRequiredMixin,generic.ListView):
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
			"isItPrivate": message.isItPrivate,
			"is_encrypted": message.is_encrypted,
			"message": message,
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
			private_public = form.cleaned_data['privacy']
			encryption = form.cleaned_data['encryption']
			public_key = ""
			encrypted_msg_filename = ""
			if private_public == 'Private':
				privacy = True
				if encryption == 'Encrypted':
					is_encrypted = True
					public_key = RSA.importKey(user.public_key)
					cipher = PKCS1_OAEP.new(public_key)
					ciphertext = cipher.encrypt(message_body.encode())
					encrypt_filename = os.getcwd() + "/catalog/encrypted_messages/" + user.username
					with open (encrypt_filename, 'wb+') as f:
						f.write(ciphertext)
					encrypted_msg_filename = encrypt_filename
					decrypted_msg_filename = os.getcwd() + "/catalog/decrypted_messages/" + user.username
					with open (decrypted_msg_filename, 'wb+') as f:
						f.write(b"")
					message_text = "Message is encrypted. Download file to view message."
				else:
					is_encrypted = False
					message_text = message_body
			else:
				privacy = False
				is_encrypted = False
				message_text = message_body
			message = Message(
				recipient=user,
				message_body=message_text,
				isItPrivate = privacy,
				is_encrypted=is_encrypted,
				public_key=public_key,
				encrypted_msg_filename=encrypted_msg_filename,
				decrypted_msg_filename=decrypted_msg_filename,
			)
			message.save()
			return HttpResponse("message saved", message)
		else:
			return HttpResponse(form.errors.as_data())
	else:
		form = CreateMessageForm()

	return render(request, 'create_message.html', {'form': form})


@csrf_exempt
def download_message(request, message_id):
	if request.method == 'POST':
		form = DownloadMessageForm(request.POST)
		try:
			message = Message.objects.get(pk=message_id)
		except Exception as e:
			return HttpResponse(e)
		if form.is_valid():
			private_key_string = form.cleaned_data['private_key']
			private_key =  '-----BEGIN RSA PRIVATE KEY-----\n'+ private_key_string.replace(' ','\n') + '\n-----END RSA PRIVATE KEY-----'
			private_key_object = RSA.importKey(private_key)
			decrypt_cipher = PKCS1_OAEP.new(private_key_object)
			with open(message.encrypted_msg_filename, 'rb') as f:
				ciphertext = b""
				chunk_size = 8192
				while True:
					chunk = f.read(chunk_size)
					if len(chunk) == 0:
						break
					ciphertext += chunk
			decrypted_message = decrypt_cipher.decrypt(ciphertext)
			filename = message.decrypted_msg_filename + message.recipient.username
			with open(filename, 'wb') as f:
				f.write(decrypted_message)
			response = HttpResponse(content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(message.recipient.username)
			response.write(decrypted_message)
			return response
		else:
			return HttpResponse(form.errors.as_data())
	else:
		form = DownloadMessageForm()

	return render(request, 'decrypt_message.html', {'form': form})


@csrf_exempt
def delete_message(request, message_id):
	try:
		message = Message.objects.get(pk=message_id)
		message.delete()
		return HttpResponse("message deleted", True)
	except:
		return HttpResponse("message does not exist", False)


class GroupsByUserListView(LoginRequiredMixin,generic.ListView):
	model = Group
	template_name ='catalog/list_groups.html'
	paginate_by = 10


@csrf_exempt
def group_detail(request, group_name):
	try:
		group = Group.objects.get(pk=group_name)
		users = group.users.split(',')
		actual_users = []
		all_users = User.objects.all()
		for u in all_users: 
			if u.username in users:
				actual_users.append(u)

		reports = group.reports.split(',')
		actual_reports = []
		all_reports = Report.objects.all()
		for r in all_reports:
			if r.report_name in reports:
				actual_reports.append(r)

		context = {
			"name": group.name,
			"users": actual_users,
			"reports": actual_reports,
			"id": group_name,
		}
		return render(request, 'catalog/detailedgroup.html', context=context)
	except Exception as e:
		return HttpResponse(e)


@csrf_exempt
def create_group(request):
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			form_users = form.cleaned_data['users']
			form_name = form.cleaned_data['group_name']
			form_reports = form.cleaned_data['group_reports']
			rep = ""
			users = ""
			for u in form_users:
				users = users + u.username + ',' 
			for r in form_reports:
				rep = rep + r.report_name + ','
			group = Group(
				name = form_name,
				users = users,
				reports = rep,
			)
			group.save()
			return HttpResponse("group saved", {'group': group})
		else:
			return HttpResponse(form.errors.as_data())
	else:
		form = CreateGroupForm()

	return render(request, 'create_group.html', {'form': form})

def remove_from_group(request, group_name, uname):
	group = Group.objects.get(pk=group_name)
	users = group.users.split(',')
	users.remove(uname)
	new_users = ""
	for u in users: 
		new_users = new_users + u + ','
	group.users = new_users
	group.save()
	return render(request, 'remove_user.html')

def my_groups(request, uname):
	groups = Group.objects.all()
	in_groups = []
	if uname == 'admin':
		in_groups = groups
	else:
		for g in groups:
			users = g.users.split(',')
			if uname in users:
				in_groups.append(g)
	context = {
		'list_groups':in_groups,
	}
	return render(request,'catalog/list_groups.html', context=context)