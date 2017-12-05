from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
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
from PIL import Image
from io import BytesIO
import random
import os
import hashlib

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

@csrf_exempt
def search(request):
	template_name = "search.html"
	form = searchForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			try:
				a = form.cleaned_data['search']
				rep = []
				try:
					rep.extend(Report.objects.filter(
						Q(report_name = a) |
						Q(company_name = a) |
						Q(company_phone = a) |
						Q(company_industry=a)|
						Q(company_location=a)|
						Q(company_sector=a)|
						Q(company_country=a)|
						Q(current_projects=a)|
						Q(info = a)|
						Q(owner = a)
					))
				except:
					pass

			except Exception as e:
				return HttpResponse(e)
		return render(request, 'catalog/list_results.html', {'reports': rep, 'search': a})
	else:
		form = searchForm()
	return render(request, template_name, {'form': form})


class ReportsByUserListView(LoginRequiredMixin,generic.ListView):
	model = Report
	template_name ='catalog/list_reports.html'
	paginate_by = 10

class FavoritesByUserListView(LoginRequiredMixin,generic.ListView):
	model = Report
	template_name ='catalog/list_favorites.html'
	paginate_by = 10

@csrf_exempt
def report_detail(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		encode_name = hashlib.sha1(report.report_name.encode('utf-8'))
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
			"privacy_setting": report.privacy_setting,
			"timestamp": report.timestamp,
			"files" : for_report_files,
            'get_comments_url': report.get_comments_url,
            'create_comments_url': report.create_comments_url,
            'id' : report_id,
            'current_rating' : report.rating,
            'num_ratings' : report.num_ratings,
            'owner' : report.owner,
		}
		if report.hash_name == encode_name.hexdigest():
			return render(request, 'catalog/detailedreport.html', context=context)
		else:
			return HttpResponse("this report has been tampered with.")
	except Exception as e:
		return HttpResponse(e)

from django.core.files.storage import FileSystemStorage

@csrf_exempt
def add_to_favorites(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		request.user.favorites.add(report)
		return render(request, 'catalog/list_favorites.html')

	except Exception as e:
		return HttpResponse(e)

@csrf_exempt
def remove_from_favorites(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		request.user.favorites.remove(report)
		return render(request, 'catalog/list_favorites.html')

	except Exception as e:
		return HttpResponse(e)

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
            hash_n = hashlib.sha1(report_name.encode('utf-8'))
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
					hash_name = hash_n.hexdigest()
				)
                report.save()
                for f in files:
                	new_file = File(file = f)
                	new_file.report = report.id
                	new_file.save()
                return redirect('encrypt_files', report_id=report.id)
            except Exception as e:
                return HttpResponse("exception", False)
        # else:
        #     return HttpResponse(form.cleaned_data['filename'])
    else:
        form = CreateReportForm()
    return render(request, 'create_report.html', {'form': form})

@csrf_exempt
def encrypt_files(request, report_id):
	files = File.objects.all()
	relevant_files = []
	for f in files:
		if f.report == report_id:
			relevant_files.append(f)
	context = {
		"files" : relevant_files,
	}
	if request.method=="POST":
		for key in request.POST.keys():
			if key != 'none':
				file = File.objects.get(pk=key)
				file.encrypted = True
				file.save()
		return HttpResponse("report saved")
	return render(request, "encrypt_files.html", context=context)

@csrf_exempt
def edit_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    files = File.objects.all()
    for_report_files = []
    for f in files:
    	if f.report == report_id:
    		for_report_files.append(f)
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
    	'files' : for_report_files,
    	'id' : report_id,
    	# 'file_name' : report.filename,
    }
    if request.method == 'POST':
        form = EditReportForm(request.POST, request.FILES)
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
            new_files = request.FILES.getlist('filename')
            for f in new_files:
              	new_file = File(file = f)
              	new_file.report = report.id
              	new_file.save()
            return HttpResponse("report updated", True)
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = EditReportForm()
    return render(request, 'edit_report.html', context= {'form': form, 'context':context}, )

def add_files(request, report_id):
    if request.method == 'POST':
        form = addFiles(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('filename')
            try:
                for f in files:
                	new_file = File(file = f)
                	new_file.report = report_id
                	new_file.save()
                return HttpResponse("files added")
            except Exception as e:
                return HttpResponse("exception", False)
        # else:
        #     return HttpResponse(form.cleaned_data['filename'])
    else:
        form = addFiles()
    return render(request, 'add_files.html', {'form': form})

@csrf_exempt
def delete_report(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		report.delete()
		return HttpResponse("report deleted", True)
	except:
		return HttpResponse("report does not exist", False)

@csrf_exempt
def rate_report(request, report_id):
	report = Report.objects.get(pk=report_id)
	context = {
		"name" : report.report_name,
		"current_rating" : report.rating,
	}
	if request.method == 'POST':
		stars = request.POST.get('rating')
		curr_rating = report.rating
		total = curr_rating*report.num_ratings
		report.num_ratings += 1
		if stars == "half":
			total += 0.5
		elif stars == "1 and a half":
			total += 1.5
		elif stars == "2 and a half":
			total += 2.5
		elif stars == "3 and a half":
			total += 3.5
		elif stars == "4 and a half":
			total += 4.5
		else:
			total += int(stars)
		new_rating = total/report.num_ratings
		report.rating = new_rating
		report.save()
		return HttpResponse("thank you for rating this report", True)
	return render(request, 'rate.html', context=context)

def delete_file(request, file_id, report_id):
	try:
		file = File.objects.get(pk=file_id)
		file.delete()
		return HttpResponse("file deleted", True)
	except:
		return HttpResponse("file does not exist", False)

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
			"encrypted_message_body": message.encrypted_message_body.decode(errors='ignore'),
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
			user2 = User.objects.get(username=form.cleaned_data['sender'])
			message_body = form.cleaned_data['message_body']
			private_public = form.cleaned_data['privacy']
			encryption = form.cleaned_data['encryption']
			public_key = ""
			encrypted_msg_filename = ""
			if private_public == 'Private':
				privacy = True
				if encryption == 'Encrypted':
					is_encrypted = True
					message_text = "Message is encrypted."
					if privacy and is_encrypted:
						public_key = RSA.importKey(user.public_key)
						cipher = PKCS1_OAEP.new(public_key)
						ciphertext = cipher.encrypt(message_body.encode())
						encrypted_message_body = ciphertext
				else:
					is_encrypted = False
					message_text = message_body
			else:
				privacy = False
				is_encrypted = False
				message_text = message_body
			message = Message(
				recipient=user,
				sender=user2,
				message_body=message_text,
				encrypted_message_body=encrypted_message_body,
				isItPrivate=privacy,
				is_encrypted=is_encrypted,
				public_key=public_key,
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
			ciphertext = message.encrypted_message_body
			decrypted_message = decrypt_cipher.decrypt(ciphertext)
			response = HttpResponse(content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(message.recipient.username + str(message_id))
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

def add_user(request, group_name):
	if request.method == "POST":
		form = AddUserForm(request.POST)
		if form.is_valid():
			form_user = form.cleaned_data['user']
			group = Group.objects.get(pk=group_name)
			all_users = User.objects.all()
			usernames = []
			for u in all_users:
				usernames.append(u.username)
			users = group.users.split(',')
			if form_user in usernames and form_user not in users:
				users.append(form_user)
			new_users = ""
			for u in users:
				new_users = new_users + u + ','
			group.users = new_users
			group.save()
			return HttpResponse("group saved", {'group': group})
		else:
			return HttpResponse(form.errors.as_data())
	else:
		form = AddUserForm()

	return render(request, 'add_user.html', {'form': form})


def remove_from_group(request, group_name, uname):
	group = Group.objects.get(pk=group_name)
	users = group.users.split(',')
	users.remove(uname)
	context = {
		'group_name' : group.name,
		'username' : uname,
	}
	new_users = ""
	for u in users:
		new_users = new_users + u + ','
	group.users = new_users
	group.save()
	return render(request, 'remove_user.html', context=context)

def my_groups(request, uname):
	groups = Group.objects.all()
	users = User.objects.all()
	user = User()
	for u in users:
		if u.username == uname:
			user = u
	in_groups = []
	if user.user_type == 'manager':
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
