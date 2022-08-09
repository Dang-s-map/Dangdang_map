from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=32, verbose_name='사용자 아이디', unique=True)
    password = models.CharField(max_length=64, verbose_name='사용자 비밀번호', null=True)
    email = models.EmailField(max_length=128, verbose_name='사용자 이메일', null=True)
    # 유저 부분 


class Location(models.Model):
    locationName = models.CharField(max_length=100)

class Cafe(models.Model):
    cafeName= models.CharField(max_length=100)
    cafePhone= models.CharField(max_length=100)
    cafeAddress= models.CharField(max_length=100)
    cafeLink= models.CharField(max_length=100)
    cafeImg= models.CharField(max_length=100)
    cafeCategory= models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Place(models.Model):
    placeName = models.CharField(max_length=100)
    placePic = models.CharField(max_length=100)
    placeAddress = models.CharField(max_length=100)
    placePhone = models.CharField(max_length=100)
    placeLink = models.CharField(max_length=100)
    placeCategory = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Accomodation(models.Model):
    accomodationName = models.CharField(max_length=100)
    AccomodationAddress = models.CharField(max_length=100)
    AccomodationImg = models.CharField(max_length=100)
    AccomodationCategory = models.CharField(max_length=100)
    AccomodationLink = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Medical(models.Model):
    medicalName = models.CharField(max_length=100)
    medicalPhone = models.CharField(max_length=100)
    medicalAddress = models.CharField(max_length=100)
    medicalLocation = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Post(models.Model):
    postType = models.CharField(max_length=100)
    postGood= models.CharField(max_length=100)
    postBad= models.CharField(max_length=100)
    postImage= models.CharField(max_length=100)
    ranking= models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Accomodation, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)