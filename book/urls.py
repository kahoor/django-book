from django.urls import path, re_path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.BookListView.as_view(), name='booklist'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='bookdetail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='loanedbooksbyuser'),
    path('<uuid:pk>/renew/', views.renew_book_librarian, name="bookrenew"),
    re_path(r'get/', views.APIListCreateBook.as_view(), name='bookslistapi'),
    re_path(r'^update/(?P<pk>\d+)/$', views.ApiRetrieveUpdateDestroyBook.as_view(), name='bookudapi')
]
