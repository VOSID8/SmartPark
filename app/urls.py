from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('add-data/<slug:slug>/', views.addData, name = 'add_data'),
    path('vehicle-info/<slug:slug>/', views.vehicleInfo, name = 'vehicle_info'),
    path('revenue/', views.revenue, name = 'revenue'),
    path('contact/', views.contact, name = 'contactpage'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
]