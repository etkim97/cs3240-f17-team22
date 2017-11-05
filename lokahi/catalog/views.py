from django.shortcuts import render

# Create your views here.

from .models import User, Report, Message

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



from django.views import generic

class ReportListView(generic.ListView):
    model = Report
    paginate_by = 10

class ReportDetailView(generic.DetailView):
    model = Report


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
    Generic class-based view accessible reports to current user. 
    """
    model = Message
    template_name ='catalog/list_messages.html'
    paginate_by = 10


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

from .forms import RenewBookForm


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

#     return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})



