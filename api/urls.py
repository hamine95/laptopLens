from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns=[
    path('add-cpu',AddCPUView.as_view()),
    path('cpu',CPUView.as_view()),
]
