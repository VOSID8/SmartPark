from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('add-data/<slug:event>/<slug:type>/', views.addData, name = 'add_data'),
    path('vehicle-info/<slug:slug>/', views.vehicleInfo, name = 'vehicle_info'),
    path('revenue/', views.revenue, name = 'revenuepage'),
    path('contact/', views.contact, name = 'contactpage'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
    path('about/', views.about, name = 'aboutpage'),
    path('video-stream/<slug:event>/<slug:type>/', views.videoStream, name='video_camera'),
    path('live-cam/<slug:event>/<slug:type>/', views.liveCam, name = 'live_camera')
]