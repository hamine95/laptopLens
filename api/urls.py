from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns=[
    path('add/cpu',AddCPUView.as_view()),
    path('cpu',CPUView.as_view()),

    path('add/ram',AddRAMView.as_view()),
    path('ram',RAMView.as_view()),

    path('add/disc',AddDiscView.as_view()),
    path('disc',DISCView.as_view()),

    path('add/laptop',AddDLaptopView.as_view()),
    path('laptop',LaptopView.as_view()),

    path('add/location',AddDLocationView.as_view()),
    path('location',LocationView.as_view()),

    path('add/store',AddStoreView.as_view()),
    path('store',Storeiew.as_view()),

    path('add/announcement',AddAnnouncementView.as_view()),
    path('announcement',AnnouncementView.as_view()),    
]
