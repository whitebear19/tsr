from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Uploadedcsv(models.Model):
    id=models.AutoField(primary_key=True)
    user_id = models.CharField(default='',max_length=255, null=True)    
    filename = models.CharField(default='',max_length=255, null=True)
    file = models.FileField(upload_to='csv',default='', null=True) 
    created_at = models.DateTimeField(auto_now_add=True,blank=True) 
    class Meta:
        db_table = 'uploadedcsv'

class Uploadedpdb(models.Model):
    id=models.AutoField(primary_key=True)
    user_id = models.CharField(default='',max_length=255, null=True)    
    filename = models.CharField(default='',max_length=255, null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True) 
    class Meta:
        db_table = 'uploadedpdb'
