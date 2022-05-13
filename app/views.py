from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Vehicle, Contact, Parking, Revenue
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'app/base.html')

def loginView(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR, "Wrong username or password!")
            return redirect("/login")
        login(request, user)
        return redirect("/")
    return render(request, 'app/login.html')

def logoutView(request):
    logout(request)
    return redirect("/login")

def addData(request, event, type):
    if request.method=="POST":
        if parking.parkingsVacant==0:
            messages.add_message(request, messages.ERROR, "Parking full!")
            return redirect(f"/add-data/{event}/{type}")
        number = request.POST.get('number')
        number = number.upper()
        parking = Parking.objects.get(user = request.user)
        if event=='arrival':
            entryTime = request.POST.get('entryTime')
            entryTime = datetime.strptime(entryTime, "%Y-%m-%dT%H:%M").replace(second = 0, microsecond = 0)
            entry = Vehicle(number = number, entryTime = entryTime, user = request.user, type = type)
            parking.parkingsOccupied += 1
            parking.parkingsVacant -= 1
        else:
            exitTime = request.POST.get('exitTime')
            exitTime = datetime.strptime(exitTime, "%Y-%m-%dT%H:%M").replace(second = 0, microsecond = 0)
            entry = Vehicle.objects.filter(user = request.user, number = number, exitTime = None).last()
            if entry is None:
                messages.add_message(request, messages.ERROR, "Invalid number")
                return redirect(f"/add-data/{event}/{type}")
            entry.exitTime = exitTime
            entry.parkingDuration = str(exitTime - entry.entryTime)
            parking.parkingsOccupied -= 1
            parking.parkingsVacant += 1
        entry.save()
        parking.save()
        messages.add_message(request, messages.SUCCESS, "Entry added succesfully.")
        return redirect(f"/add-data/{event}/{type}")
    if event=='arrival':
        if type=='car':
            return render(request, 'app/NewData.html')
        else:
            return render(request, 'app/arr2W.html')
    elif type=='car':
        return render(request, 'app/departure.html')
    return render(request, 'app/dep2W.html')

def revenue(request):
    return render(request, 'app/Revenue.html')

def vehicleInfo(request, slug):
    data = Vehicle.objects.filter(user=request.user, type=slug)
    parking = Parking.objects.get(user = request.user)
    p = Paginator(data, 20)
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    data = p.page(page)
    if slug=='car':
        return render(request, 'app/infoPage.html', {
            'data': data,
            'parking': parking
        })
    return render(request, 'app/2Wheelers.html', {
            'data': data,
            'parking': parking
        })

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
    return render(request, 'app/contactUs.html')

def about(request):
    return render(request, 'app/aboutUs.html')