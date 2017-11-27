from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^myreports/$', views.ReportsByUserListView.as_view(), name='my_reports'),
    url(r'^report/(?P<report_id>[0-9]+)$', views.report_detail, name='report_detail'),
    url(r'^report/create$', views.create_report, name='create_report'),
    url(r'^report/edit/(?P<report_id>[0-9]+)$', views.edit_report, name='edit_report'),
    url(r'^report/delete/(?P<report_id>[0-9]+)$', views.delete_report, name='delete_report'),

    url(r'^mymessages/$', views.MessagesByUserListView.as_view(), name='my_messages'),
    url(r'^message/(?P<message_id>[0-9]+)$', views.message_detail, name='message_detail'),
    url(r'^message/create$', views.create_message, name='create_message'),
    url(r'^message/delete/(?P<message_id>[0-9]+)$', views.delete_message, name='delete_message'),

    url(r'^mygroups/$', views.GroupsByUserListView.as_view(), name='my_groups'),
    url(r'^group/create$', views.create_group, name='create_group'),
    url(r'^group/(?P<group_name>[\w\-]+)$', views.group_detail, name='group_detail'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^users/$', views.users, name='users'),
    url(r'^suspend/(?P<uname>[\w\-]+)$', views.suspend, name='suspend')
]
