from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from forms.py import reportForm

# Create your views here.

from .models import User, Report, Message
from .forms import *
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    # num_reports=Report.objects.all().count()
    # num_messages=Message.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_visits':num_visits},
    )

def createAccount(request):
    return render(
        request,
        'create_account.html',
        )

from django.views import generic

class ReportListView(generic.ListView):
    model = Report
    paginate_by = 10

class ReportDetailView(generic.DetailView):
    model = Report
    template_name = 'catalog/detailedreport.html'

from django.contrib.auth.mixins import LoginRequiredMixin

class ReportsByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view accessible reports to current user.
    """
    model = Report
    template_name ='catalog/list_reports.html'
    paginate_by = 10

    # Need to get user reports by privacy accessibility

    # def get_queryset(self):
    #     return Report.objects.filter(user=self.request.user).filter(status__exact='o').order_by('due_back')


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class MessageDetailView(generic.DetailView):
    model = Message
    template_name = 'catalog/detailmessage.html'

class MessageCreate(CreateView):
    model = Message
    fields = '__all__'
    success_url = '/'


class MessageUpdate(UpdateView):
    model = Message
    fields = ['recipient', 'message_body']
    success_url = '/'

class MessageDelete(DeleteView):
    model = Message
    success_url = reverse_lazy('messages')


class MessagesByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view accessible messages to current user.
    """
    model = Message
    template_name ='catalog/list_messages.html'
    paginate_by = 10


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.db import models
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = signUp(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.company = form.cleaned_data['company']
            user.password=form.cleaned_data['password']
            user.email = form.cleaned_data['email']
            user.user_type = form.cleaned_data['user_type']
            user.save()
            # print(form.cleaned_data['username'])
            return redirect('/')
    else:
        form = signUp()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def report(request):
    if request.method == 'POST':

        return redirect('index')
    return render(request, 'report.html')

@csrf_exempt
def message(request):
    if request.method == 'POST':
        return redirect('index')
    return render(request, 'message.html')



# Use this template to update reports

# @permission_required('catalog.can_mark_returned')
# def renew_book_librarian(request, pk):
#     """
#     View function for renewing a specific BookInstance by librarian
#     """
#     book_inst=get_object_or_404(BookInstance, pk = pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_inst.due_back = form.cleaned_data['renewal_date']
#             book_inst.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect('/')

#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

<<<<<<< HEAD
#     return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
=======
#     return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
>>>>>>> 767863616310a2fa46b4b2959a0c1e16e5aa9da0
