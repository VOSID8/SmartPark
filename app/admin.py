from django.contrib import admin
from app import models

# Register your models here.

@admin.register(models.Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['number', 'type', 'entryTime', 'exitTime', 'parkingDuration', 'user']
    ordering = ['number', 'type', 'entryTime', 'exitTime', 'parkingDuration', 'user']
    list_filter = ['user', 'type']

@admin.register(models.Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'totalParkings', 'parkingsAvailable', 'parkingsOccupied', 'parkingsVacant']
    ordering = ['user', 'totalParkings', 'parkingsAvailable']

@admin.register(models.Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'amount']
    list_ordering = ['user', 'date', 'amount']
    list_filter = ['user']

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'time']
    ordering = ['name', 'time']