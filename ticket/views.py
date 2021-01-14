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
from ticket.models import Uploadedcsv,Uploadedpdb
from Main import settings

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains                  

import urllib.request
import pandas as pd


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
def start(filename): 
    files = Uploadedpdb.objects.all()
    if files:        
        files.delete()

    non_functional_urls = []
    data = []
    start = time.time()
    media_root = settings.MEDIA_ROOT
    pdb_root = os.path.join(media_root, 'pdb')
    media_root = os.path.join(media_root, 'csv')
    
    
    #arr = ['1h7w', '1jmx', '1rq6', '2j9u', '1d9c', '2ciw']
    samples_file = pd.read_csv(os.path.join(media_root, filename))

    sample = samples_file['protein'].map(str).values

    for id in sample: 
        #Generate the downloadable URL
        url = "http://files.rcsb.org/download/{}.pdb".format(id.replace(
                '+', ''))
        #Check if the URL exists, otherwise skip that PDB ID
        request = requests.get(url)
        if request.status_code == 200:
            outputFilename = "{}/{}.pdb".format(pdb_root,str(id.replace('+', '')))
            response = urllib.request.urlopen(url)
            zippedData = response.read()
            # save data to disk
            output = open(outputFilename,'wb')
            
            output.write(zippedData)
            output.close()
            
            temp = url + " extracted to " + outputFilename
            print(temp)
            thisfilename = str(id.replace('+', '')) + ".pdb"
            row = Uploadedpdb(user_id='1',filename=thisfilename)
            row.save()
            print(thisfilename)
            data.append(temp)
            
        else:
            non_functional_urls.append(id)
            continue
    if non_functional_urls:
        msg = "Un available URLs- {}".format(non_functional_urls)
        data.append(msg)
        print(msg)
    msg = 'Downloaded {}/{} PDB files and saved at {}'.format(
            len(sample) - len(non_functional_urls), len(sample), 
            os.path.join(pdb_root))
    data.append(msg)
    
    msg = 'Time taken for generating sample is {} mins.'.format(
            round((time.time()-start)/60, 2))
    data.append(msg)

    
    return data
       
def upload_csv(request):
    data = ''
    try:    
        files = Uploadedcsv.objects.all()
        if files:
            for item in files:
                try:
                    print(item.filename)
                    print(settings.MEDIA_ROOT)            
                    media_root = settings.MEDIA_ROOT
                    media_root = os.path.join(media_root, 'csv')
                    filename = item.filename
                    os.remove(os.path.join(media_root, filename))
                except:
                    pass
            files.delete()
        
        filename = request.FILES.get('attach').name
        row = Uploadedcsv(user_id='1',file=request.FILES.get('attach'),filename=filename)
        row.save()
        filename = str(row.file) 
        filename = filename.replace('csv/','')   
        row.filename = filename               
        row.save() 
        data = filename
        return JsonResponse({'results':True,'data':data})
    except:
        return JsonResponse({'results':False,'data':data}) 

def process_csv(request):

    data = []
    try:    
                
        filename = request.POST.get('filename')
        print(filename)
        if filename:        
            data = start(filename)

        
        return JsonResponse({'results':True,'data':data})    
    except:
        return JsonResponse({'results':False,'data':data}) 