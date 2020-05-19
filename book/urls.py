from django.urls import path, re_path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.BookListView.as_view(), name='booklist'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='bookdetail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='loanedbooksbyuser'),
    path('<uuid:pk>/renew/', views.renew_book_librarian, name="bookrenew"),
]
