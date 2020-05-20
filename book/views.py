import datetime
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy


# this is for times a url can only access by users and the the view is functionbase
from django.contrib.auth.decorators import login_required
# this is for times a url can only access by some soort of vip user or somthing like that
from django.contrib.auth.decorators import user_passes_test
# this is for times a url can only access by some soort of vip user or somthing like that
from django.contrib.auth.decorators import permission_required

# this is for times a url can only access by users and the the view is generic base
from django.contrib.auth.mixins import LoginRequiredMixin
# this is for times a url can only access by some soort of vip user or somthing like that
from django.contrib.auth.mixins import UserPassesTestMixin
# this is for times a url can only access by some soort of vip user or somthing like that
from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import generics

from .serializers import BookSerializer
from .forms import RenewBookForm

from .models import Book
from .models import BookInstance
from .models import Author
from .models import Ganre
# Create your views here.

def email_chek(user):
    return user.email.endswith("@yahoo.com")

@login_required
@user_passes_test(email_chek)
@permission_required('can_read_ps')
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_ganre = Ganre.objects.count()  
    
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_ganre': num_ganre,
    }

    return render(request, 'book/index.html', context)

@login_required
@permission_required('librarian')
def renew_book_librarian(request, pk):
    book_ins = get_object_or_404(BookInstance, pk=pk)

    if request.method=="POST":
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_ins.due_back = form.cleaned_data['renewaldate']
            book_ins.save()

            return HttpResponseRedirect(reverse_lazy('book:booklist'))

    else:
        p_rd = datetime.date.today()+datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewaldate': p_rd})
    
    context = {
        'form': form,
        'book_ins': book_ins
    }

    return render(
        request,
        'book/renewaldate.html',
        context
    )



# this type of views are caled generic_display, you can find them in document
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    """
    ok so by default it will make a context_object_name = 'book_list' 
    and will pass it to a template_name = 'book/book_list.html'
    but we can define them manually and change things up if we neet to
    """
    # we can filter the query set or any other changes
    # queryset = Book.objects.filter(title__icontains = 'rich')[:3]

    # or by overiding some shits
    def get_queryset(self):
        queryset = super(BookListView, self).get_queryset()
        # icontains is not case sensetive but contains is
        # queryset = Book.objects.filter(title__icontains = 'the')[:3]# TODO
        queryset = Book.objects.all()
        return queryset


    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['other_book_list'] = Book.objects.all()
        return context
    

class BookDetailView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, generic.DetailView):
    model = Book
    permission_required = 'can_read_ps'

    def test_func(self):
        return self.request.user.email.endswith("yahoo.com")


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'book/bookinstance_list_borrower.html'
    paginate_by = 2
    
    def get_queryset(self):
        queryset = super(LoanedBooksByUserListView, self).get_queryset()
        queryset = queryset.filter(borrower=self.request.user).order_by('due_back')
        return queryset


class APIListCreateBook(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class ApiRetrieveUpdateDestroyBook(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
