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
    path('store',view=views.store, name='store'),
    path('get_tickets',view=views.get_tickets, name='get_tickets'),
    path('delete',view=views.delete, name='delete'),   
    path('ischecklicense',view=views.ischecklicense, name='ischecklicense'),   
    path('get_stake',view=views.get_stake, name='get_stake'),
   
]