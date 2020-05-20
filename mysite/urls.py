
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', views.signup, name='signup'),
    re_path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/books/', include('book.urls', namespace='booksapi')),
]
