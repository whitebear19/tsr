from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'ticket'
urlpatterns = [                   
    path('dashboard',view=views.dashboard, name='dashboard'),
    path('calculate',view=views.calculate, name='calculate'),
    path('clustering',view=views.clustering, name='clustering'),
    path('identify',view=views.identify, name='identify'),
    path('view_existing_samples',view=views.view_existing_samples, name='view_existing_samples'),
    path('edit/<str:id>',view=views.edit, name='edit'),
    # ajax
    path('upload_csv',view=views.upload_csv, name='upload_csv'),   
    path('process_csv',view=views.process_csv, name='process_csv'), 
   
]