from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.

class AddCPUView(generics.CreateAPIView):
    queryset=CPU.objects.all()
    serializer_class=CPUSerializer

class AddRAMView(generics.CreateAPIView):
    queryset=Ram.objects.all()
    serializer_class=RAMSerializer

class AddDiscView(generics.CreateAPIView):
    queryset=Disc.objects.all()
    serializer_class=DiscSerializer

class AddDLaptopView(generics.CreateAPIView):
    queryset=Laptop.objects.all()
    serializer_class=LaptopSerializer

class AddDLocationView(generics.CreateAPIView):
    queryset=Location.objects.all()
    serializer_class=LocationSerializer

class AddStoreView(generics.CreateAPIView):
    queryset=Store.objects.all()
    serializer_class=StoreSerializer

class AddAnnouncementView(generics.CreateAPIView):
    queryset=Announcement.objects.all()
    serializer_class=AnnouncementSerializer

class CPUView(generics.ListAPIView):
    queryset=CPU.objects.all()
    serializer_class=CPUSerializer

class RAMView(generics.ListAPIView):
    queryset=Ram.objects.all()
    serializer_class=RAMSerializer

class DISCView(generics.ListAPIView):
    queryset=Disc.objects.all()
    serializer_class=DiscSerializer
    
class LaptopView(generics.ListAPIView):
    queryset=Laptop.objects.all()
    serializer_class=LaptopSerializer

class LocationView(generics.ListAPIView):
    queryset=Location.objects.all()
    serializer_class=LocationSerializer

class Storeiew(generics.ListAPIView):
    queryset=CPU.objects.all()
    serializer_class=StoreSerializer

class AnnouncementView(generics.ListAPIView):
    queryset=Announcement.objects.all()
    serializer_class=AnnouncementSerializer
 