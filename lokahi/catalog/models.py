from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.


class User(AbstractUser):
	username = models.CharField(max_length=200, default="none", unique=True)
	password = models.CharField(max_length=200, default="none")
	first_name = models.CharField(max_length=200, default="none")
	last_name = models.CharField(max_length=200, default="none")
	company = models.CharField(max_length=200, default="none")
	email = models.EmailField(max_length=200, default="none")
	user_type = models.CharField(max_length=10, default=1)
	is_suspended = models.BooleanField(default = False)
	def __str__(self):
		return "%s - %s - %s - %s" % (self.username,
			self.password, self.first_name, self.last_name)

from django.urls import reverse_lazy
# Used to generate URLS by reversing the URL patterns

class Report(models.Model):
	report_name = models.CharField(max_length=200)
	company_name = models.CharField(max_length=40)
	company_phone = models.CharField(max_length=15)
	company_location = models.CharField(max_length=40)
	company_country = models.CharField(max_length=40)
	company_sector = models.CharField(max_length=40)
	company_industry = models.CharField(max_length=40)
	current_projects = 	models.TextField(help_text = "Enter a list of the current projects")
	info = models.TextField(help_text = "Enter information about the business plan and/or project")
	owner = models.CharField(max_length=50, default="admin")
	# Need to actually upload the file here
	filename = models.FileField()

	# Need to set private/public through user settings here
	privacy_setting = models.CharField(max_length=10)
	timestamp = models.DateTimeField(auto_now_add = True)


	# Need to allow investor users to upload files

	def __str__(self):
		return self.report_name

	def get_absolute_url(self):
		return reverse_lazy('report_detail', args=[str(self.id)])

	def get_edit_url(self):
		return reverse_lazy('edit_report', args=[str(self.id)])

	def get_delete_url(self):
		return reverse_lazy('delete_report', args=[str(self.id)])

	def get_comments_url(self):
		return reverse_lazy('report_comments', args=[str(self.id)])
		

class Comment(models.Model):
	report = models.ForeignKey(Report, related_name='comments')
	author = models.ForeignKey(User)
	text = models.TextField()

	def __str__(self):
		return "Comment by " + str(self.author)


# A user can leave a private message for a specific user. A user will have the ability to see a list of
# messages left for him or her, and be able to delete a message. Private messages will be encrypted, and
# the recipient can choose to decrypt it and then read

class Message(models.Model):
	"""
	Model representing a message between users
	"""

	recipient = models.ForeignKey(User, on_delete = models.CASCADE)
	message_body = models.TextField(help_text = "Enter your private message.")
	isItPrivate = models.BooleanField(default=True)

	def __str__(self):
		return "Message for " + str(self.recipient.username)

	def get_absolute_url(self):
		return reverse_lazy('message_detail', args=[str(self.id)])

	def get_delete_url(self):
		return reverse_lazy('delete_message', args=[str(self.id)])



class Group(models.Model):
	"""
	Model representing groups that users can create
	"""

	name = models.CharField(max_length=50, default="group")
	users = models.CharField(max_length=50, default="admin")
	group_reports = models.CharField(max_length=50, default="report")
	#users = models.ManyToManyField(User)
	#reports = models.ManyToManyField(Report)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse_lazy('group-detail', args=[str(self.id)])
