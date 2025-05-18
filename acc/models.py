from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class user(AbstractUser):
    phone=models.IntegerField(unique=True,null=True,blank=True)
    is_theater_manager=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,null=True,blank=True)
    otp_verified=models.BooleanField(default=False)

