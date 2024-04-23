from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.

class AddCPUView(generics.CreateAPIView):
    queryset=CPU.objects.all()
    serializer_class=CPUSerializer

class CPUView(generics.ListAPIView):
    queryset=CPU.objects.all()
    serializer_class=CPUSerializer