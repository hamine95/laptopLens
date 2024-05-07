from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class CPU(models.Model):
    brand=models.CharField(max_length=15,null=True)
    name=models.CharField(max_length=100)
    num=models.CharField(max_length=8,null=True)

    def __str__(self):
        return f'{self.brand} {self.name} {self.num}'
    
    def add_new_cpu(name):
        cpu=CPU.objects.filter(name=name)
        if not cpu.exists():
            cpu=CPU(name=name)
            cpu.save()
            return cpu
        else:
            return cpu.first()

class Ram(models.Model):
    memory_standard=models.CharField(max_length=8,null=True)
    size=models.CharField(null=False)
    def __str__(self):
        return f'{self.memory_standard} {self.size}'
    
    def add_new_ram(size):
        ram = Ram.objects.filter(size=size)
        if not ram.exists():
            ram=Ram(size=size)
            ram.save()
            return ram
        else:
            return ram.first()

class Disc(models.Model):
    tech_type=models.CharField(max_length=25)
    size=models.CharField(null=False)
    def __str__(self):
        return f'{self.tech_type} {self.size}'
    
    def add_new_disc(size,disc_type="HDD"):
        disc=Disc.objects.filter(size=size, tech_type=disc_type)
        if not disc.exists():
            disc=Disc(size=size, tech_type=disc_type)
            disc.save()
            return disc
        else:
            return disc.first()

class Laptop(models.Model):
    brand=models.CharField(max_length=50,null=True)
    brand_model=models.CharField(max_length=15,null=True)
    reference=models.CharField(max_length=20,null=True)
    cpu=models.ForeignKey(CPU,on_delete=models.CASCADE)
    ram=models.ForeignKey(Ram,on_delete=models.CASCADE)
    disk=models.ForeignKey(Disc,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.brand} {self.brand_model}'
    
    def add_new_laptop(brand, ram, cpu, disc):
        laptop=Laptop.objects.filter(brand=brand, ram=ram, cpu=cpu, disk=disc)
        if not laptop.exists():
            laptop=Laptop(brand=brand, ram=ram, cpu=cpu, disk=disc)
            laptop.save()
            return laptop
        else:
            return laptop.first()


class Location(models.Model):
    address=models.CharField(max_length=250)
    wilaya=models.CharField(max_length=100)
    def __str__(self):
        return f'{self.address} {self.wilaya}'
    
    def add_new_location(address, wilaya):
        location=Location.objects.filter(address=address,wilaya=wilaya)
        if not location.exists():
            location=Location(address=address, wilaya=wilaya)
            location.save()
            return location
        else:
            return location.first()

class Store(models.Model):
    name=models.CharField(max_length=50)
    slug=models.CharField(max_length=50)
    description=models.CharField(max_length=800,null=True)
    image_url=models.CharField(max_length=150,null=True)
    url=models.CharField(max_length=150,null=True)
    followers=models.IntegerField(null=True)
    annoncement_count=models.IntegerField(null=True)
    locations=models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f'{self.name}'
    
    def add_new_store(name, slug, description, locations, image_url=None, url=None, followers=None, annoncement_count=None):
        store=Store.objects.filter(name=name, slug=slug, description=description)
        if not store.exists():
            store=Store(name=name, slug=slug, description=description, image_url=image_url
                                ,url=url,followers= followers, annoncement_count= annoncement_count, locations= locations)
            store.save()
            return store
        else:
            return store.first()

class Announcement(models.Model):
    original_id=models.IntegerField(default=1)
    laptop=models.ForeignKey(Laptop,on_delete=models.CASCADE)
    store=models.ForeignKey(Store,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=300,null=True)
    created_at=models.DateTimeField()
    like_count=models.IntegerField(null=True)
    description=models.CharField(max_length=2000,null=True)
    has_delivery=models.BooleanField(default=False)
    price=models.IntegerField(default=1)
    medias=ArrayField(models.CharField(max_length=200,null=True),5,null=True)
    def __str__(self):
        return f'pc:{self.laptop}, store:{self.store}, date:{self.created_at}, likes:{self.like_count}'
    
    def add_new_announcement(id,laptop, store, title, created_at, like_count, description, has_delivery, price, medias):
        announcement=Announcement.objects.filter(original_id=id)
        if not announcement.exists():
            announcement=Announcement(original_id=id, laptop=laptop, title=title, created_at=created_at
                                ,like_count=like_count,description= description, has_delivery= has_delivery, price= price,medias=medias)
            announcement.save()
            return announcement
        else:
            return announcement.first()