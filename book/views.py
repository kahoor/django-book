from django.shortcuts import render
from django.views import generic

from .models import Book
from .models import BookInstance
from .models import Author
from .models import Ganre
# Create your views here.

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


class BookListView(generic.ListView):
    model = Book