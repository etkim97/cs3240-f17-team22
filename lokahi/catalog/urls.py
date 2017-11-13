from django.conf.urls import url
from catalog import views, views_reports, views_messages


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^myreports/$', views.ReportsByUserListView.as_view(), name='my-reports'),
    url(r'^myreports/(?P<pk>\d+)$', views.ReportsByUserListView.as_view(), name='report-detail'),

    url(r'^mymessages/$', views.MessagesByUserListView.as_view(), name='my-messages'),
    #add URL detail for messages

    url(r'^report/(?P<report_id>[0-9]+|(all))$', views_report.report, name='report'),
    url(r'^report/create$', views_report.create_report, name='create_report'),
    url(r'^report/delete/(?P<report_id>[0-9]+)$', views_book.delete_report, name='delete_report'),
]

urlpatterns += [
    url(r'^signup/$', views.signup, name='signup'),
]



urlpatterns += [
url(r'^report/$', views.report, name='report'),
]
urlpatterns += [
url(r'^message/$', views.message, name='message'),
]
########

# urlpatterns += [
#     url(r'^$', views.index, name='index'),
#     url(r'^books/$', views.BookListView.as_view(), name='books'),
#     url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
# ]

# urlpatterns += [   
#     url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
# ]

# urlpatterns += [  
#     url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
#     url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
#     url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
# ]