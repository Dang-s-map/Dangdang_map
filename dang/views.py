from asyncio.windows_events import NULL
from http.client import HTTPResponse
from re import template
from unicodedata import category
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.db.models import Q
import csv
from .models import User, Post, Cafe, Place, Accomodation, Medical, Location

from .forms import PostForm


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email.policy import default
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

from .models import User, Location, Cafe, Place, Accomodation, Medical, Post 

def login(request):

    if request.method == 'POST':
        아이디 = request.POST['username']
        비밀번호 = request.POST['password']

        user = auth.authenticate(request, username=아이디, password=비밀번호)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})
    return render(request, 'login.html')

def join(request):
    if request.method == 'POST' :
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username = request.POST['username'],
                password = request.POST['password1'],
                email = request.POST['email'],
            )

            auth.login(request, user)
            return redirect('/')
        return render (request, 'join.html')
    return render (request, 'join.html')
def logout(request):
    auth.logout(request)
    return redirect('/')


def mypage(request):

    return render(request, 'mypage.html')

# 임시로 만들어 둔 지역 list입니다. 나중에 db로 대체하든, 얘기해봐요..
locationDic = {'seoul':'서울','gyeongi':'경기','incheon':'인천','gangwon':'강원','chungbuk':'충북','chungnam':'충남','deajeon':'대전','sejong':'세종','jeonbuk':'전북','jeonnam':'전남','gwangju':'광주','gyeongbuk':'경북','gyeongnam':'경남','daegu':'대구','ulsan':'울산','busan':'부산','daejeon':'대전','jeju':'제주' }

def home(request):
    locationList = locationDic.values()

    context = { "locationList" : locationList }

    return render(request,'home.html', context=context)

def cafeList(request):
    #
    only_cate_cafe=Cafe.objects.filter(Q(location='서울')&Q(type='애견동반'))
    context = { "category" : "cafe", "location" : NULL, 'list' : only_cate_cafe}
    #
    #
    return render(request, 'mainList.html', context=context)

def placeList(request):
    #
    only_cate_place=Place.objects.filter(Q(location='서울')& Q(type='명소'))
    context = { "category" : "place", "location" : NULL, 'list' : only_cate_place}
    #
    #
    return render(request, 'mainList.html', context=context)

def accomoList(request):
    #
    only_cate_accom=Accomodation.objects.filter(Q(location='서울')& Q(type='호텔'))
    context = { "category" : "accomo", "location" : NULL , 'list' : only_cate_accom}
    #
    #
    return render(request, 'mainList.html', context=context)

def detail(request):
    #
    #
    #
    return render(request, 'detail.html')

def mainList(request):
    #
    context = { "category" : "medical", "location" : NULL }
    #
    #
    return render(request, 'medicalList.html', context=context)

def mainList(request, location): # main에서 지역 선택했을 때
    #
    only_loc= Cafe.objects.filter(Q(location=location)& Q(type='애견동반'))
    context = { "location" : location, 'list' : only_loc }
    #
    #
    return render(request, 'mainList.html', context=context)

def medicalList(request): # main에서 지역 선택했을 때
    #
    #
    #
    return render(request, 'medicalList.html')

@csrf_exempt
def cates(request):
    req = json.loads(request.body)
    cate = req['cate'] # 카페, 숙소, 장소
    return JsonResponse({'cate' : cate})

@csrf_exempt
def locationBtn(request):
    return JsonResponse({})


## list page에서 ajax 처리했을 때
# 수정 필요: 용어? 통일
# @csrf_exempt
# def listGo(request):
#     req = json.loads(request.body)
#     loc = req['location'] # 강원,경기,제주 등등 17개 도
#     cate = req['category'] # cafe, accommodation, place
#     type = req['detail'] # (애견동반, 애견전용) or (공원, 명소) 등등

    # if cate == 'cafe':
    #     cafes= Cafe.objects.filter(Q(location=loc)& Q(type=type))
    #     context = {'list' : cafes }
    # elif cate == 'accommodation':
    #     accommos= Accomodation.objects.filter(Q(location=loc)& Q(type=type))
    #     context = {'list' : accommos }  
    # elif cate == 'place':
    #     places= Place.objects.filter(Q(location=loc)& Q(type=type))
    #     context = {'list' : places }
    
    # for place in list:

    
    # JsonResponse(context)

def cafeToDictionary(list):
    output = {}
    output["name"] = list.name
    output["location"] = list.location
    output["address"] = list.address
    output["phone"] = list.phone
    output["type"] = list.type
    output["menuInfo"] = list.menuInfo
    output["hourInfo"] = list.hourInfo
    output["link1"] = list.link1
    output["desc"] = list.desc
    # output["img"] = str(list.img)
    output["mapx"] = list.mapx
    output["mapy"] = list.mapy
    return output

def placeToDictionary(list):
    output = {}
    output["name"] = list.name
    output["location"] = list.location
    output["address"] = list.address
    output["phone"] = list.phone
    output["star"] = list.star
    output["link1"] = list.link1
    output["link2"] = list.link2
    output["type"] = list.type
    output["desc"] = list.desc
    # output["img"] = str(list.img)
    output["mapx"] = list.mapx
    output["mapy"] = list.mapy
    return output


## list page에서 ajax 처리했을 때
# 수정 필요: 용어? 통일
@csrf_exempt
def listGo(request):
    req = json.loads(request.body)
    loc = req['location'] # 강원,경기,제주 등등 17개 도
    cate = req['category'] # cafe, accommodation, place
    type = req['detail'] # (애견동반, 애견전용) or (공원, 명소) 등등
    # 여기서 data 처리해서 반환해주세요
    print(req,loc,cate,type)
    if cate == 'cafe': 
        # cafes = Cafe.objects.filter(Q(location=loc) & Q(type=type))
        cafes=Cafe.objects.filter(Q(location=loc) & Q(type=type))
        tempCafe = []
        for i in range(len(cafes)):
            tempCafe.append(cafeToDictionary(cafes[i]))
        list = tempCafe
    elif cate == 'accomodation':
        accomos = Accomodation.objects.filter(Q(location=loc) & Q(type=type))
        tempAccomo = []
        for i in range(len(accomos)):
            tempAccomo.append(placeToDictionary(accomos[i]))
        list = tempAccomo
    elif cate == 'place':
        places = Place.objects.filter(Q(location=loc) & Q(type=type))
        tempPlace = []
        for i in range(len(places)):
            tempPlace.append(placeToDictionary(places[i]))
        list = tempPlace
    
    data = {'list':list}
    # 아래는 test용 JsonResponse 입니다. 수정필요
    return JsonResponse(data)
    
    

    # 아래는 test용 JsonResponse 입니다. 수정필요
    # return JsonResponse(context)

## 상세페이지 부분 입니다. (cafeDetail, accommoDetail, placeDetail)
def cafeDetail(request, id):
    cafe = Cafe.objects.get(id=id)
    context = { "cafe":cafe }
    return render(request, '무슨무슨.html', context=context)
    
def accommoDetail(request, id):
    accomo = Accomodation.objects.get(id=id)
    context = { "accomo":accomo }
    return render(request, '무슨무슨.html', context=context)

def placeDetail(request, id):
    place = Place.objects.get(id=id)
    context = { "place":place }
    return render(request, '무슨무슨.html', context=context)




### db에 csv 파일 넣는 함수입니다.
### migrations 날리고 dbsqlite 날리고 사용해야 합니다. 한번만 작동해주세요..!! 여러번 하면 여러번 들어가요
def csvToModel(request):
    c = open("./static/csv/cafe.csv",'r',encoding='CP949')
    a = open("./static/csv/accommo.csv",'r',encoding='CP949')
    p = open("./static/csv/place.csv",'r',encoding='CP949')
    
    reader_cafe = csv.reader(c)
    reader_accomo = csv.reader(a)
    reader_place = csv.reader(p)

    cafes = []
    places = []
    accomos = []

    for row in reader_accomo:
        accomos.append(Accomodation(name=row[0],location=row[1],address=row[2],phone=row[3],star=row[4],link1=row[5],link2=row[6],type=row[7],desc=row[8],img=row[9][0],mapx=row[10],mapy=row[11]))
    Accomodation.objects.bulk_create(accomos)

    for r in reader_cafe:
        try:
            cafes.append(Cafe(name=r[0],location=r[1],address=r[2],phone=r[3],type=r[4],menuInfo=r[5],hourInfo=r[6],link1=r[7],desc=r[8],img=r[9],mapx=r[10],mapy=r[11]))
        except:
            cafes.append(Cafe(name=r[0],location=r[1],address=r[2],phone=r[3],type=r[4],menuInfo=r[5],hourInfo=r[6],link1=r[7],desc=r[8],img=r[9]))
    Cafe.objects.bulk_create(cafes)

    for r in reader_place:
        places.append(Place(name=r[0],location=r[1],address=r[2],phone=r[3],star=r[4],link1=r[5],link2=r[6],type=r[7],desc=r[8],img=r[9],mapx=r[10],mapy=r[11]))
    Place.objects.bulk_create(places)


    c.close()
    a.close()
    p.close()

    return HttpResponse('create model~')

    ##### 멍초이스 작성

def create(request, category, categry_id):
    if category == "Cafe":
        post = Cafe.objects.get(id=categry_id)
    if category == "Accomodation":
        post = Accomodation.objects.get(id=categry_id)
    if category == "Place":
        post = Place.objects.get(id=categry_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save()
            post.save()
            return redirect('/cafe 상세페이지')
    else:
        form=PostForm()
    return render(request, 'dang/mainList.html', {'form':form , 'post':post})


