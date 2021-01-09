from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Tickets(models.Model):
    id=models.AutoField(primary_key=True)
    username = models.CharField(default='',max_length=255, null=True, unique=True)    
    license_key = models.CharField(default='',max_length=255, null=True)
    expire = models.CharField(default='',max_length=255, null=True)
    connections = models.CharField(default='',max_length=255, null=True,)
    bookie = models.CharField(default='',max_length=255, null=True)    
    status = models.CharField(default='',max_length=255, null=True)    
    created_at = models.DateTimeField(auto_now_add=True,blank=True) 
    class Meta:
        db_table = 'tickets'
