from django.db import models
import sys
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), null=True,default='')    
    created_at = models.DateTimeField(auto_now_add=True,blank=True)



     
