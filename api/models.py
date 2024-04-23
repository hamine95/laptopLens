from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class CPU(models.Model):
    brand=models.CharField(max_length=15,null=True)
    name=models.CharField(max_length=15)
    num=models.CharField(max_length=8)

class Ram(models.Model):
    memory_standard=models.CharField(max_length=8)
    size=models.IntegerField(null=False)

class Disc(models.Model):
    tech_type=models.CharField(max_length=8)
    size=models.IntegerField(null=False)

class Laptop(models.Model):
    reference=models.CharField(max_length=20)
    cpu=models.ForeignKey(CPU,on_delete=models.CASCADE)
    ram=models.ForeignKey(Ram,on_delete=models.CASCADE)
    disk=models.ForeignKey(Disc,on_delete=models.CASCADE)
    price=models.IntegerField()
    has_delivery=models.BooleanField()
    medias=ArrayField(models.CharField(max_length=10),5)


class Location(models.Model):
    address=models.CharField(max_length=20)
    wilaya=models.CharField(max_length=20)

class Store(models.Model):
    name=models.CharField(max_length=20)
    slug=models.CharField(max_length=20)
    description=models.CharField(max_length=30)
    image_url=models.CharField(max_length=30)
    url=models.CharField(max_length=30)
    followers=models.IntegerField()
    annoncement_count=models.IntegerField()
    locations=models.ForeignKey(Location,on_delete=models.CASCADE)

class Announcement(models.Model):
    laptop=models.ForeignKey(Laptop,on_delete=models.CASCADE)
    store=models.ForeignKey(Store,on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField()
    
    