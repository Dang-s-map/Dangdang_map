from email.policy import default
from operator import mod
from tabnanny import verbose
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=32, verbose_name='사용자 아이디', unique=True)
    password = models.CharField(max_length=64, verbose_name='사용자 비밀번호', null=True)
    email = models.EmailField(max_length=128, verbose_name='사용자 이메일', null=True)
    # 유저 부분 

# class Location(models.Model):
#     locationName = models.CharField(max_length=100)

class Cafe(models.Model):
    name= models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address= models.CharField(max_length=100)
    phone= models.CharField(max_length=100, null=True)
    star = models.CharField(max_length=100, null=True)
    type= models.CharField(max_length=100, null=True)
    menuInfo = models.TextField(null=True)
    hourInfo = models.TextField(null=True)
    link1 = models.TextField(null=True)
    desc = models.TextField(null=True)
    img= models.ImageField(upload_to='', null=True)
    mapx = models.CharField(max_length=100, null=True)
    mapy = models.CharField(max_length=100, null=True)
    favorite = models.BooleanField(default=False) # 임시 필드?


class Place(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=True)
    star = models.CharField(max_length=100, null=True)
    link1 = models.TextField(null=True)
    link2 = models.TextField(null=True)
    type = models.CharField(max_length=100, null=True)
    desc = models.TextField(null=True)
    img = models.ImageField(upload_to='', null=True)
    mapx = models.CharField(max_length=100, null=True)
    mapy = models.CharField(max_length=100, null=True)
    favorite = models.BooleanField(default=False) # 임시 필드?


class Accomodation(models.Model):
    name = models.CharField(max_length=100)
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True)
    star = models.CharField(max_length=100, null=True)
    link1 = models.TextField(null=True)
    link2 = models.TextField(null=True)
    type = models.CharField(max_length=100, null=True)
    desc = models.CharField(max_length=255, null=True)
    img = models.ImageField(upload_to='', null=True)
    mapx = models.CharField(max_length=100, null=True)
    mapy = models.CharField(max_length=100, null=True)
    favorite = models.BooleanField(default=False) # 임시 필드?
    

class Medical(models.Model):
    medicalName = models.CharField(max_length=100)
    medicalPhone = models.CharField(max_length=100)
    medicalAddress = models.CharField(max_length=100)
    medicalLocation = models.CharField(max_length=100)
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Post(models.Model):
    postType = models.CharField(max_length=100, null=True)
    postImage= models.ImageField(blank=True, default="NULL", upload_to='posts/%Y%m%d', verbose_name="사진")
    postGood= models.TextField(null=True)
    postBad= models.TextField(null=True)
    ranking= models.IntegerField(null=True)
    user = models.ForeignKey(User, related_name='user_post', on_delete=models.CASCADE)
    placeId = models.IntegerField(null=True)
    # cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='cafe_post', null=True)
    # place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_post', null=True)
    # accomo = models.ForeignKey(Accomodation, on_delete=models.CASCADE, related_name='accomo_post', null=True)


# 찜하기
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    like = models.BooleanField(default=False)
    placeType = models.CharField(max_length=50) # 여기에 cafe, accommo, place 세 개만 들어오게! 아니면 choicefeild로 해도 되구
    placeId = models.IntegerField()