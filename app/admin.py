from django.contrib import admin
from app import models

# Register your models here.

@admin.register(models.Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['number', 'type', 'entryTime', 'exitTime', 'parkingDuration']
    ordering = ['number', 'type', 'entryTime', 'exitTime', 'parkingDuration']
    list_filter = ['user', 'type']

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'time']
    ordering = ['name', 'time']