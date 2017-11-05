from django.contrib import admin

# Register your models here.

from .models import User, Report, Message

# Define the admin class
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name')

# Register the admin class with the associated model
admin.site.register(User, UserAdmin)


# Define the admin class
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'info', 'filename', 'privacy_setting')

# Register the admin class with the associated model
admin.site.register(Report, ReportAdmin)

# # Register the Admin classes for Book using the decorator

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message_body')
