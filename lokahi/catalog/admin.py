from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from .models import User, Report, Message, Comment, Group, File

# Define the admin class
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name', 'user_type')

# Register the admin class with the associated model
admin.site.register(User, UserAdmin)


# Define the admin class

class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'info', 'privacy_setting', 'owner')

# Register the admin class with the associated model
admin.site.register(Report, ReportAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('report', 'author', 'text')

admin.site.register(Comment, CommentAdmin)

class FileAdmin(admin.ModelAdmin):
	list_display = ('file', 'report')

admin.site.register(File, FileAdmin)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message_body')

