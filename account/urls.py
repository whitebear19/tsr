from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'account'
urlpatterns = [       
    path('check_register',view=views.check_register, name='check_register'),
    path('check_login',view=views.check_login, name='check_login'),
   
    path('',view=views.index, name='index'),
    path('logout',view=views.logout, name='logout'),
          
    
]