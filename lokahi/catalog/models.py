from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.


class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)

	def __str__(self):
		return "%s - %s - %s - %s" % (self.username, 
			self.password, self.first_name, self.last_name)	


from django.urls import reverse_lazy
# Used to generate URLS by reversing the URL patterns

class Report(models.Model):
	"""
	Model representing a report (but not a specific copy of a book).
	"""
	report_name = models.CharField(max_length=200)
	company_name = models.CharField(max_length=40)
	company_phone = models.CharField(max_length=15)
	company_location = models.CharField(max_length=40)
	company_country = models.CharField(max_length=40)
	company_sector = models.CharField(max_length=40)
	company_industry = models.CharField(max_length=40)
	current_projects = 	models.TextField(help_text = "Enter a list of the current projects")
	info = models.TextField(help_text = "Enter information about the business plan and/or project")

	# Need to actually upload the file here
	filename = models.CharField(max_length=200)

	# Need to set private/public through user settings here
	privacy_setting = models.CharField(max_length=10)
	timestamp = models.DateTimeField(auto_now_add = True)


	# Need to allow investor users to upload files

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return self.report_name

	def get_absolute_url(self):
		"""
		Returns the url to access a particular report instance.
		"""
		return reverse_lazy('report-detail', args=[str(self.id)])


# A user can leave a private message for a specific user. A user will have the ability to see a list of
# messages left for him or her, and be able to delete a message. Private messages will be encrypted, and
# the recipient can choose to decrypt it and then read 

class Message(models.Model):
	"""
	Model representing a message between users
	"""

	recipient = models.ForeignKey(User, on_delete = models.CASCADE)
	message_body = models.TextField(help_text = "Enter your private message.")

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return "Message for " + str(self.recipient.username)

	def get_absolute_url(self):
		"""
		Returns the url to access a particular report instance.
		"""
		return reverse_lazy('message-detail', args=[str(self.id)])







