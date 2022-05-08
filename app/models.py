from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    type = models.CharField(max_length = 15)
    number = models.CharField(max_length = 15)
    entryTime = models.DateTimeField(auto_now = True)
    exitTime = models.DateTimeField(null = True)
    parkingDuration = models.DateTimeField(null = True)

class Contact(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    time = models.DateTimeField(auto_now = True)
    phone = models.CharField(max_length = 13)
    message = models.TextField()