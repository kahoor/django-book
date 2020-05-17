
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', views.signup, name='signup')
]
