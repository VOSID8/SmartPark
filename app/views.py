from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Vehicle, Contact, Parking, Revenue
from datetime import datetime, date
from .camera import VideoCamera
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

# Create your views here.

@login_required
def index(request):
    return render(request, 'app/homePage.html')

def loginView(request):
    next = request.GET.get('next')
    if next is None:
        next = '/'
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR, "Wrong username or password!")
            return redirect("/login")
        login(request, user)
        return redirect(next)
    return render(request, 'app/login.html', {"next": next})

def logoutView(request):
    logout(request)
    return redirect("/login")

#add entry and exit time minually
@login_required
def addData(request, event, type):
    parking = Parking.objects.get(user = request.user, type = type)
    if request.method=="POST":
        if parking.parkingsVacant==0:
            messages.add_message(request, messages.ERROR, "Parking full!")
            return redirect(f"/add-data/{event}/{type}")
        number = request.POST.get('number')
        number = number.upper()
        if event=='arrival':
            entryTime = request.POST.get('entryTime')
            entryTime = datetime.strptime(entryTime, "%Y-%m-%dT%H:%M").replace(second = 0, microsecond = 0)
            entry = Vehicle(number = number, entryTime = entryTime, user = request.user, type = type)
            parking.parkingsOccupied += 1
            parking.parkingsVacant -= 1
            rev = Revenue.objects.filter(user=request.user, date=entryTime.date()).first()
            if rev is None:
                rev = Revenue(user=request.user, date=entryTime.date(), amount=30)
            else:
                rev.amount += 30
            rev.save()
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

@login_required
def revenue(request):
    data = Revenue.objects.filter(user=request.user)
    todayRevenue = Revenue.objects.filter(user=request.user, date=date.today()).first()
    if todayRevenue is None:
        todayRevenue = 0
    else:
        todayRevenue = todayRevenue.amount
    totalRevenue = 0
    for d in data:
        totalRevenue += d.amount
    p = Paginator(data, 20)
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    data = p.page(page)
    prev = 0
    next = 0
    if page<p.num_pages:
        next = page+1
    if page>0:
        prev = page-1
    return render(request, 'app/Revenue.html', {
        'data': data,
        'curr': page,
        'pages': p.page_range,
        'prev': prev,
        'next': next,
        'today_revenue': todayRevenue,
        'total_revenue': totalRevenue
    })

@login_required()
def vehicleInfo(request, slug):
    data = Vehicle.objects.filter(user = request.user, type = slug)
    parking = Parking.objects.get(user = request.user, type = slug)
    p = Paginator(data, 20)
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    data = p.page(page)
    prev = 0
    next = 0
    if page<p.num_pages:
        next = page+1
    if page>0:
        prev = page-1
    if slug=='car':
        return render(request, 'app/infoPage.html', {
            'data': data,
            'parking': parking,
            'curr': page,
            'pages': p.page_range,
            'next': next,
            'prev': prev
        })
    return render(request, 'app/2Wheelers.html', {
            'data': data,
            'parking': parking,
            'curr': page,
            'pages':  p.page_range,
            'next': next,
            'prev': prev
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
    return render(request, 'app/contactUs2.html')

def about(request):
    return render(request, 'app/aboutUs.html')

@login_required
def liveCam(request, event, type):
    return render(request, 'app/liveCam.html', {'event': event, 'type': type})

def addEntry(request, number, event, type):
    time = datetime.now().replace(second=0, microsecond=0)
    parking = Parking.objects.get(user=request.user, type=type)
    if event=='arrival':
        entry = Vehicle.objects.filter(number=number).last()
        if entry is not None and entry.exitTime is not None:
            return
        if parking.parkingsVacant==0:
            return
        entry = Vehicle(number=number, type=type, user=request.user, entryTime=time)
        parking.parkingsOccupied += 1
        parking.parkingsVacant -= 1
        rev = Revenue.objects.filter(user=request.user, date=date.today()).first()
        if rev is None:
            rev = Revenue(user=request.user, date=date.today(), amount=30)
        else:
            rev.amount += 30
        rev.save()
    else:
        entry = Vehicle.objects.filter(number=number, type='car').last()
        entry.exitTime = time
        entry.parkingDuration = str(time - entry.entryTime)
        parking.parkingsOccupied -= 1
        parking.parkingsVacant += 1
    entry.save()
    parking.save()

def gen(camera, request, event, type):
    while True:
        img = camera.get_frame()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) 
        edged = cv2.Canny(bfilter, 30, 200) 
        # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                # print("Hnji")
                location = None
                for contour1 in contours:
                    approx = cv2.approxPolyDP(contour1, 10, True)
                    if len(approx) == 4:
                        location = approx
                        break
                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [location], 0,255, -1)
                new_image = cv2.bitwise_and(img, img, mask=mask)
                # plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
                (x,y) = np.where(mask==255)
                (x1, y1) = (np.min(x), np.min(y))
                (x2, y2) = (np.max(x), np.max(y))
                cropped_image = gray[x1:x2+1, y1:y2+1]
                # plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
                reader = easyocr.Reader(['en'])
                if reader==True: 
                    result = reader.readtext(cropped_image)
                    # print(result)
                    text = result[0][-2]
                    # print(text)
                    addEntry(request, text, event, type)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
                    cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
                    # plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
                    # plt.show()
                # print("done")
        # img = cv2.flip(img, 1)
        _, frame = cv2.imencode('.jpg', img)
        frame = frame.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required
def videoStream(request, event, type):
    return StreamingHttpResponse(gen(VideoCamera(), request, event, type),
                    content_type='multipart/x-mixed-replace; boundary=frame')