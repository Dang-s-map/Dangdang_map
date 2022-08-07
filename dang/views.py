from django.shortcuts import render

def home(request):
    return render(request,'home.html')

def cafeList(request):
    #
    #
    #
    return render(request, 'cafeList.html')

def accomodationList(request):
    #
    #
    #
    return render(request, 'accomodationList.html')

def placeList(request):
    #
    #
    #
    return render(request, 'placeList.html')

def detail(request):
    #
    #
    #
    return render(request, 'detail.html')

def list(request):
    #
    #
    #
    return render(request, 'list.html')


###############################
# csv 파일 import

import csv

from django.shortcuts import render
from django.http import HttpResponse

# db 모델들.. 여기서는 Nutrition만 쓸 예정
from .models import *

data = None
file_dir = 'C:/Users/손병우/Desktop/Daedong_Mung!/data.csv'

def read_data(request):
    with open(file_dir,'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        global data
        for row in reader:
            if row[0]:
                cafe_name_csv=row[0]
            # if row[1]:
            #     cafe_review_csv=row[1]
                print(cafe_name_csv)
                Cafe.objects.create(cafeName = cafe_name_csv)
    return render(request, 'list.html')
    