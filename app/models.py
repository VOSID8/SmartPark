from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    type = models.CharField(max_length = 15)
    number = models.CharField(max_length = 15)
    entryTime = models.DateTimeField()
    exitTime = models.DateTimeField(null = True)
    parkingDuration = models.CharField(max_length = 70, null = True)

    def __str__(self):
        return str(self.number)

class Parking(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    type = models.CharField(max_length=15)
    totalParkings = models.PositiveBigIntegerField()
    parkingsAvailable = models.PositiveBigIntegerField()
    parkingsOccupied = models.PositiveBigIntegerField()
    parkingsVacant = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.user)

class Revenue(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField()
    amount = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.user)

class Contact(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    time = models.DateTimeField(auto_now = True)
    phone = models.CharField(max_length = 13)
    message = models.TextField()