from rest_framework import serializers
from .models import *

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model=CPU
        fields=('brand','name','num')

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ram
        fields=('memory_standard','size')

class DiscSerializer(serializers.ModelSerializer):
    class Meta:
        model=Disc
        fields=('tech_type','size')

class LaptopSerializer(serializers.ModelSerializer):
    #ram = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Laptop
        fields=('reference','price','has_delivery','medias','cpu','ram','disk')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=('address','wilaya')

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Store
        fields=('name','slug','description','image_url','url','locations')

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Announcement
        fields=('laptop','store','created_at')
