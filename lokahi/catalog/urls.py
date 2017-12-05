from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^acceptprivileges/(?P<uname>[\w\-]+)$', views.accept_privileges, name='accept_privileges'),

    url(r'^myreports/$', views.ReportsByUserListView.as_view(), name='my_reports'),
    url(r'^myreports/favorites/$', views.FavoritesByUserListView.as_view(), name='my_favorites'),
    url(r'^report/(?P<report_id>[0-9]+)$', views.report_detail, name='report_detail'),
    url(r'^report/(?P<report_id>[0-9]+)/favorite$', views.add_to_favorites, name='add_to_favorites'),
    url(r'^myreports/favorites/remove_from_favorites$', views.remove_from_favorites, name='remove_from_favorites'),
    url(r'^report/(?P<report_id>[0-9]+)/rate$', views.rate_report, name='rate_report'),
    url(r'^report/(?P<report_id>[0-9]+)/addfiles$', views.add_files, name='add_files'),
    url(r'^report/create$', views.create_report, name='create_report'),
    url(r'^report/encrypt/(?P<report_id>[0-9]+)$', views.encrypt_files, name='encrypt_files'),
    url(r'^report/edit/(?P<report_id>[0-9]+)$', views.edit_report, name='edit_report'),
    url(r'^report/edit/(?P<report_id>[0-9]+)/delete/(?P<file_id>[0-9]+)$', views.delete_file, name='delete_file'),
    url(r'^report/delete/(?P<report_id>[0-9]+)$', views.delete_report, name='delete_report'),
    url(r'^report/comments/(?P<report_id>[0-9]+)$', views.get_comments, name='report_comments'),
    url(r'^report/comments/create/(?P<report_id>[0-9]+)$', views.create_comment, name='create_comment'),

    url(r'^mymessages/$', views.MessagesByUserListView.as_view(), name='my_messages'),
    url(r'^message/(?P<message_id>[0-9]+)$', views.message_detail, name='message_detail'),
    url(r'^message/create$', views.create_message, name='create_message'),
    url(r'^message/delete/(?P<message_id>[0-9]+)$', views.delete_message, name='delete_message'),
    url(r'^message/download/(?P<message_id>[0-9]+)$', views.download_message, name='download_message'),
    url(r'^message/decrypt$', views.download_message, name='decrypt_message'),

    url(r'^mygroups/(?P<uname>[\w\-]+)$', views.my_groups, name='my_groups'),
    url(r'^group/create$', views.create_group, name='create_group'),
    url(r'^group/(?P<group_name>[0-9]+)$', views.group_detail, name='group_detail'),
    url(r'^group/(?P<group_name>[0-9]+)/remove/(?P<uname>[\w\-]+)$', views.remove_from_group, name='remove_from_group'),
    url(r'^group/(?P<group_name>[0-9]+)/add_user', views.add_user, name='add_user'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/privileges/(?P<uname>[\w\-]+)$', views.privileges, name='privileges'),
    url(r'^suspend/(?P<uname>[\w\-]+)$', views.suspend, name='suspend'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_messages/$', views.search_message, name='search_message'),
]
