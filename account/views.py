from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import math
import requests
import time
import datetime
import json
import os 
import random
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm

from account.models import CustomUser

import datetime
from datetime import timedelta
import random
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from PIL import Image
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def get_different_time(orgtime):
    
    curtime = datetime.datetime.now()
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    date1 = orgtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    date2 = curtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    diff = datetime.datetime.strptime(date2, datetimeFormat)\
        - datetime.datetime.strptime(date1, datetimeFormat)    
    
    result = ''
    if(int(diff.days) > 0):
        result = diff.days       
        if(int(result)>30):
            result = math.ceil(int(result)/30)
            result = str(result)+"Months"
        else:
            result = str(result)+"Days"
    else:
        result = diff.seconds
        if(int(result) > 3600):
            result = math.ceil(int(result)/3600)
            result = str(result)+"Hours"
        else:
            result = math.ceil(int(result)/60)+1
            result = str(result)+"Mins"
    return result

def get_date_str(orgtime):
    result = ''
    curtime = datetime.datetime.now()
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    date1 = orgtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    date2 = curtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    diff = datetime.datetime.strptime(date2, datetimeFormat)\
        - datetime.datetime.strptime(date1, datetimeFormat)        
    if(int(diff.days) < 1):
        curDate = curtime.strftime('%d')
        orgDate = orgtime.strftime('%d')
        if curDate == orgDate:
            result = 'Today'
        else:
            result = 'Yesterday'
    elif (int(diff.days) < 2):
        curDate = curtime.strftime('%d')
        orgDate = orgtime.strftime('%d')
        if int(curDate) > int(orgDate):
            if (int(curDate)-int(orgDate)) > 1:
                result = orgtime.strftime('%d%m%Y')
            else:
                result = 'Yesterday'
        else:
            result = 'Yesterday'
    else:
        result = orgtime.strftime('%d/%m/%Y')
    return result

def get_time_str(orgtime):
    result = orgtime.strftime('%H:%M')
    return result


def index(request):
    # if not request.user.is_authenticated:
    #     return redirect('/login')
    # else:        
    return redirect('/dashboard')
        
def dashboard(request):
    # if not request.user.is_authenticated:
    #     return redirect('/login')
    user = request.user 
    
    
    return render(request,'data/sample.html',{}) 
# -------------------------------------------------------
def logout(request):
    if request.method == 'POST':
        auth_views.auth_logout(request)
    return redirect('/login')



# ajax_part

def check_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    results = {}
    
    is_check = 0
    
    is_check = CustomUser.objects.filter(username=username).count()
    if is_check > 0:
        cur_user = CustomUser.objects.get(username=username)
    
    
    results['is_check'] = is_check    
    results['is_pass'] = '1'
    
    
    if is_check == 0 :        
        return JsonResponse({'results':results})
    else:         
        user = authenticate(username=cur_user.username,password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'results':results})

        else:            
            results['is_pass'] = '0'
            return JsonResponse({'results':results})    


def check_register(request):    
    username = request.POST.get('username').replace(" ", "")
   
    password = request.POST.get('password1')   
    is_check = CustomUser.objects.filter(username=username).count()
        

    results = {}
    results['is_check'] = is_check
        
    if is_check:
        return JsonResponse({'results':results})
    else:             
        row = CustomUser(password=make_password(password),username=username,is_superuser=0,is_staff=0,is_active=1)
        row.save() 
        return JsonResponse({'results':results})

    return JsonResponse({'results':results})


