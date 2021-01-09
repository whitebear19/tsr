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
import os,sys
import random
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

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
from ticket.models import Tickets

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains                   # For click Enter from keyboard


PAGINATION_COUNT = 10

# bet part




def is_check_username(username,id):
    if id == "0":
        rows = Tickets.objects.filter(username=username).count()
        if rows:
            return False
        else:
            return True
    else:
        rows = Tickets.objects.filter(username=username)
        if rows.count() > 1:
            return False
        elif rows.count() == 1:
            thisrow = Tickets.objects.get(username=username)
            if(thisrow.id == int(id)):
                return True
            else:
                return False   
        else:
            return True

def dashboard(request):  
    nav = 'sample'   
    
    return render(request,'data/sample.html',{'nav':nav}) 

def calculate(request):  
    nav = 'calculate'       
    return render(request,'data/calculate.html',{'nav':nav}) 

def clustering(request):  
    nav = 'clustering'       
    return render(request,'data/clustering.html',{'nav':nav}) 

def identify(request):  
    nav = 'identify'       
    return render(request,'data/identify.html',{'nav':nav}) 

def view_existing_samples(request):
    nav = 'view'       
    return render(request,'data/view_existing_samples.html',{'nav':nav})

def create(request):
    
        
    nav = 'ticket'
    return render(request,'ticket/create.html',{'nav':nav}) 

def edit(request,id):
    try:        
        row = Tickets.objects.get(id=id)        
        nav = 'ticket'
        return render(request,'ticket/create.html',{'nav':nav,'ticket':row})         
    except:
        nav = 'ticket'
        return redirect('/dashboard')

# ajax
def store(request):

    
    if not request.user.is_authenticated:
        results = False
        return JsonResponse({'results':results}) 
    else:        
        user = request.user         
        username = request.POST.get('username')
        license_key = request.POST.get('license')
        expire = request.POST.get('expire')
        connections = request.POST.get('connections')
        bookie = request.POST.get('bookie')    
        id = request.POST.get('which')

        is_valid = is_check_username(username,id)
        
        if is_valid:            
            if id == "0":
                row = Tickets(username=username,license_key=license_key,expire=expire,connections=connections,bookie=bookie)
                row.save() 
            else:
                row = Tickets.objects.get(id=id)
                row.username = username
                row.license_key = license_key
                row.expire = expire
                row.connections = connections
                row.bookie = bookie      
                row.save()
            results = True
            return JsonResponse({'results':results})    
        else:            
            return JsonResponse({'results':False,'is_username':False})  
    

def get_tickets(request):
    tickets = ''
    results = []
    pagenum = 0

    try:
               
        user = request.user
        currentPage = request.GET.get('currentPage')   
        tickets = Tickets.objects.all() 
       
        tickets = tickets.order_by('-created_at')
        pagenum = math.ceil(tickets.count()/PAGINATION_COUNT)
        paginator = Paginator(tickets,PAGINATION_COUNT)   
        resultscollection = paginator.get_page(currentPage) 
    
        for item in resultscollection:
            data = {}
            data['id'] = item.id       
            data['username'] = item.username
            data['license_key'] = item.license_key
            data['expire'] = item.expire
            data['connections'] = item.connections
            data['bookie'] = item.bookie
            data['status'] = item.status
            data['created_at'] = (item.created_at).strftime('%Y-%m-%d %H:%M:%S')            
            results.append(data)
            
        return JsonResponse({'results':results,'pagenum':pagenum})
    except:
        return JsonResponse({'results':results,'pagenum':pagenum})

def delete(request):
    try:
        id = request.GET.get('id')
        row = Tickets.objects.get(id=id)
        row.delete()
        return JsonResponse({'results':True})
    except:
        return JsonResponse({'results':False})


def ischecklicense(request):
    try:        
        username = request.GET.get('username')
        license_key = request.GET.get('license')        
        if Tickets.objects.filter(username=username).count():
            thisrow = Tickets.objects.get(username=username)
            if thisrow.license_key == license_key:
                return JsonResponse({'results':True,'username':True, 'license':True})
            else:
                return JsonResponse({'results':False,'username':True, 'license':False})
        else:
            return JsonResponse({'results':False,'username':False, 'license':False})   
        
    except:
        return JsonResponse({'results':False})


def get_stake(request):
    targetvalue = ''
    odds = ''
    stake = ''
    data = []
    try:        
        stake = request.GET.get('stake')
        print(stake)
               
        try:
            try:                
                reconnect = driver.find_elements_by_class_name('badge.badge-danger.m-2.p-2.clickable')[0]
                reconnect.click()
                time.sleep(3)
            except:
                pass
            valuebettingitem = driver.find_elements_by_class_name('odds-card.card-shadow.card-shadow-hover.d-flex.clickable.no-outline')
            for item in valuebettingitem:
                result={}
                item.click()
                time.sleep(5)
                targetvalue = driver.find_element_by_id('participants').text
                targetvalue = targetvalue.replace(" vs "," v ")         
                odds = driver.find_element_by_id('Odds').get_attribute('value')
                stake = driver.find_element_by_id('Stake').get_attribute('value')
                result['targetvalue'] = targetvalue
                result['odds'] = odds
                result['stake'] = stake
                data.append(result) 
                time.sleep(1)            
                driver.find_element_by_id('CloseSelectedCard').click()

        except:
            print('no item')
        
        return JsonResponse({'results':True,'data':data})
    except:
        return JsonResponse({'results':False,'data':data})