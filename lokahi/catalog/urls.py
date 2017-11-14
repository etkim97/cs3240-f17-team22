from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^myreports/$', views.ReportsByUserListView.as_view(), name='my_reports'),
    url(r'^report/(?P<report_id>[0-9]+)$', views.report_detail, name='report_detail'),
    url(r'^report/create$', views.create_report, name='create_report'),
    url(r'^report/delete/(?P<report_id>[0-9]+)$', views.delete_report, name='delete_report'),

    #DO SAME FOR MESSAGES HERE

    url(r'^signup/$', views.signup, name='signup'),
]

