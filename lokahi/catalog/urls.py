from django.conf.urls import url
from . import views
from . import views as core_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]

urlpatterns += [   
    url(r'^myreports/$', views.ReportsByUserListView.as_view(), name='my-reports'),
    url(r'^myreports/(?P<pk>\d+)$', views.ReportsByUserListView.as_view(), name='report-detail'),
]

urlpatterns += [   
    url(r'^mymessages/$', views.MessagesByUserListView.as_view(), name='my-messages'),
]

urlpatterns += [
    url(r'^signup/$', core_views.signup, name='signup'),
]
urlpatterns += [
url(r'^report/$', core_views.report, name='report'),
]
urlpatterns += [
url(r'^message/$', core_views.message, name='message'),
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