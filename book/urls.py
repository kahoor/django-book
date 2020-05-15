from django.urls import path, re_path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.BookListView.as_view(), name='booklist')
]
