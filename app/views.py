from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Vehicle, Contact

# Create your views here.

def index(request):
    return HttpResponse("dashboard")

def loginView(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.method.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR, "Wrong username or password!")
            return redirect("/login")
        login(user)
        return redirect("/")
    return HttpResponse('login page')

def logoutView(request):
    if request.user.is_authenticated:
        logout(request.user)
    return redirect("/login")

def addData(request, slug):
    if request.method=="POST":
        number = request.POST.get('number')
        entryTime = request.POST.get('entryTime')
        exitTime = request.POST.get('exitTime')
        if entryTime is None:
            entry = Vehicle.objects.filter(user = request.user, number = number).last()
            entry.exitTime = exitTime
            entry.parkingDuration = exitTime - entry.entrytime
        else:
            entry = Vehicle(number = number, entryTime = entryTime, user = request.user, type = slug)
        entry.save()
        messages.add_message(request, messages.SUCCESS, "Entry added succesfully.")
        return redirect(f"/add-data/{slug}")
    return HttpResponse("add data manually")

def revenue(request):
    return HttpResponse('revenue page')

def vehicleInfo(request, slug):
    data = Vehicle.objects.filter(user=request.user, type=slug)
    p = Paginator(data, 20)
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    data = p.page(1)
    return HttpResponse(data[0].number)

def contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        entry = Contact(name = name, email = email, phone = phone, message = message)
        entry.save()
        messages.add_message(request, messages.SUCCESS, "Thanks for contacting us.")
        return redirect('/contact')
    return HttpResponse('contact page')