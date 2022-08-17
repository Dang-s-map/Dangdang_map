from asyncio.windows_events import NULL
from dis import dis
import email
from http.client import HTTPResponse
from multiprocessing import context
from re import template
from unicodedata import category
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.db.models import Q, Max
import csv
from .models import User, Post, Cafe, Place, Accomodation, Medical, Like
from django.core.paginator import Paginator
from .forms import PostForm
import random


from django.core import serializers
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email.policy import default
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth
# Create your views here.


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            print("인증성공")
            auth.login(request, user)
        else:
            print("인증실패")
    return render(request, 'login.html')

def join(request):
    
    if request.method == 'POST' :
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST['email']

        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('dang:login')

    return render(request, 'join.html')

    #     if request.POST['password1'] == request.POST['password2']:
    #         user = User.objects.create_user(
    #             username = request.POST['username'],
    #             password = request.POST['password1'],
    #             email = request.POST['email'],
    #         )
    #         auth.login(request, user)
    #         return redirect('/')
    #     return render (request, 'join.html')
    # return render (request, 'join.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


# def mypage(request):

#     return render(request, 'mypage.html')

# 임시로 만들어 둔 지역 list입니다. 나중에 db로 대체하든, 얘기해봐요..
locationDic = {'seoul':'서울','gyeongi':'경기','incheon':'인천','gangwon':'강원','chungbuk':'충북','chungnam':'충남','deajeon':'대전','sejong':'세종','jeonbuk':'전북','jeonnam':'전남','gwangju':'광주','gyeongbuk':'경북','gyeongnam':'경남','daegu':'대구','ulsan':'울산','busan':'부산','jeju':'제주' }

def home(request):
    locationList = locationDic.values()
    reviews = []
    places = []
    counts = []
    
    try:
        place_ids = list(set(Post.objects.all().values_list('placeId', flat=True)))
        if len(place_ids) > 3:
            place_ids = random.sample(place_ids, 3)
            for place_id in place_ids:
                posts = Post.objects.filter(placeId=place_id)
                random_id = random.choice(posts).id
                post = Post.objects.get(id=random_id)
                if post.postType == 'cafe':
                    place = Cafe.objects.get(id=post.placeId)
                elif post.postType == 'place':
                    place = Place.objects.get(id=post.placeId)
                else :
                    place = Accomodation.objects.get(id=post.placeId)
                reviews.append(post)
                places.append(place)
                place_review = Post.objects.filter(placeId=place.id)
                counts.append(len(place_review))
        else:
            for place_id in place_ids:
                posts = Post.objects.filter(placeId=place_id)
                random_id = random.choice(posts).id
                post = Post.objects.get(id=random_id)
                if post.postType == 'cafe':
                    place = Cafe.objects.get(id=post.placeId)
                elif post.postType == 'place':
                    place = Place.objects.get(id=post.placeId)
                else :
                    place = Accomodation.objects.get(id=post.placeId)
                reviews.append(post)
                places.append(place)
                place_review = Post.objects.filter(placeId=place.id)
                counts.append(len(place_review))
        total_list=zip(reviews,places,counts)
    except:
        total_list=zip(reviews,places,counts)
        #리뷰가 하나도 없어요!
        pass                

    context = { "locationList" : locationList,"total_list": total_list}
    return render(request,'home.html', context=context)

# 메인페이지 리스팅
def toMainList(request, category, location, type):
    filteredLocation = 'nothing_yet'
    locations = locationDic.values()
    
    try:
        current_user = request.user # 현재 접속한 user를 가져온다.
        me = User.objects.get(username=current_user) # User db에서 현재 접속한 user를 찾는다.
        try:
            my_jjim_list = Like.objects.filter(Q(user=me.id) & Q(placeType=category))
        except:
            my_jjim_list = ''
    except:
        my_jjim_list = ''

    if request.method == "POST":
        location = request.POST["location"]
        category = request.POST["category"]
        type = request.POST["type"]
        return redirect(f"/list/{category}/{location}/{type}")
    else:
        if category == 'cafe':
            filteredLocation=Cafe.objects.filter(Q(location=location)&Q(type=type))
        elif category == 'place':
            filteredLocation=Place.objects.filter(Q(location=location)&Q(type=type))
        elif category == 'accomo':
            filteredLocation=Accomodation.objects.filter(Q(location=location)&Q(type=type))
				
        for i in filteredLocation:
            if my_jjim_list:   
                if i.id in my_jjim_list.values_list('placeId', flat=True):
                    jjim = Like.objects.get(Q(user=me)&Q(placeType=category)&Q(placeId=i.id))
                    i.favorite = jjim.like
                    i.save()
                else:
                    i.favorite = False
                    i.save()
            else:
                i.favorite = False
                i.save()
        
        filteredLocation = filteredLocation.order_by('id') # 가까운 순으로 정렬하면 좋을듯
        paginator = Paginator(filteredLocation, 5)   
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        context = {'category': category ,'location': location,'locations': locations, 'type': type,'posts': posts }
        return render(request, 'mainList.html', context=context)

## mainList 목록눌렀을때 상세페이지로 이동 (listDetail.html)
def listDetail(request, category, id):
    if category == 'cafe':
        here = Cafe.objects.get(id=id)
    elif category == 'place':
        here = Place.objects.get(id=id)
    elif category == 'accomo':
        here = Accomodation.objects.get(id=id)

    try:
        reviews = Post.objects.filter(placeId=id)
    except:
        reviews = '아직 리뷰가 없습니다.'
        pass
    context = {'category': category ,'here': here, 'reviews': reviews, 'name' : here.name}
    return render(request, 'listDetail.html', context=context)

def medicalList(request): # main에서 응급댕댕 선택시
    return render(request, 'medicalList.html')

@csrf_exempt
def medicals(request): # main에서 응급댕댕 선택시
    req = json.loads(request.body)
    loc = req['loc'] # 강원, 제주, 경기, 서울
    query = req['query']

    searching = loc+query
    x,y = medicalSearch(searching) # 사용자가 검색한 값의 경도,위도

    medicals = Medical.objects.filter(location=loc)

    for med in medicals:
        xx = med.x
        yy = med.y
        d = distance(x,y,xx,yy)
        Medical.objects.filter(id=med.id).update(distance=d)

    medicals = Medical.objects.filter(location=loc).order_by('distance')[:10]

    list = serializers.serialize('json',medicals)

    return JsonResponse({'list' : list, 'query':query, 'loc':loc, 'x':x,'y':y})


def update(request, id): 
    if request.method == "POST":
        postGood = request.POST["postGood"]
        postBad = request.POST["postBad"]
        postImage = request.FILES['postImage']
        ranking = request.POST["ranking"]

        Post.objects.filter(id=id).update(postGood=postGood,postBad=postBad,postImage=postImage,ranking=ranking)
        return redirect(f"reviewDetail/{id}")
    post = Post.objects.get(id=id)
    context = {"post":post}
    return render(request, "reviewWrite.html",context=context)



@csrf_exempt
def cates(request):
    req = json.loads(request.body)
    cate = req['cate'] # 카페, 숙소, 장소
    return JsonResponse({'cate' : cate})

@csrf_exempt
def btn_main(request):
    req = json.loads(request.body) 
    direction = req['direction']
    return JsonResponse({'direction': direction})


## list page에서 ajax 처리했을 때
# 수정 필요: 용어? 통일
def cafeToDictionary(list):
    output = {}
    output["name"] = list.name
    output["location"] = list.location
    output["address"] = list.address
    output["phone"] = list.phone
    output["type"] = list.type
    output["star"] = list.star
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
# @csrf_exempt
# def listGo(request):
#     req = json.loads(request.body)
#     location = req['location'] # 강원,경기,제주 등등 17개 도
#     category = req['category'] # cafe, accommodation, place
#     type = req['detail'] # (애견동반, 애견전용) or (공원, 명소) 등등
#     data = {'location':location, 'category':category, 'type':type}
#     return JsonResponse(data)
    
# 아래는 test용 JsonResponse 입니다. 수정필요
# def cafeDetail(request, id):
#     cafe = Cafe.objects.get(id=id)
#     reviews = cafe.cafe_post.all() # 역참조한건데 제대로 되나 test 해봐야 함
#     category = 'cafe'
#     context = { "cafe":cafe, "reviews":reviews, "id":id, "category":category }
#     return render(request, 'cafeDetail.html', context=context)
    


## 멍초이스 (post) 부분

def delete(request, id):
    if request.method == "POST":
        Post.objects.filter(id=id).delete()
        return redirect("/") # 삭제하고 나면 어디로 보낼까요?

def update(request, id): 
    post = Post.objects.get(id=id)
    category = post.postType
    placeId = post.placeId
    if request.method == "POST":
        postGood = request.POST["postGood"]
        postBad = request.POST["postBad"]
        postImage = request.FILES['postImage']
        ranking = request.POST["ranking"]

        Post.objects.filter(id=id).update(postGood=postGood,postBad=postBad,postImage=postImage,ranking=ranking)
        return redirect(f"/reviewDetail/{id}")
    
    if category == 'cafe':
            place = Cafe.objects.get(id=placeId)
    elif category == 'accomo':
        place = Accomodation.objects.get(id=placeId)
    else:
        place = Place.objects.get(id=placeId)

    placeName = place.name
    location=place.location

    context = {"post":post, "placeName":placeName}
    return render(request, "reviewUpdate.html", context=context)

### db에 csv 파일 넣는 함수입니다.
# 한 번만 실행.....
def csvToModel(request):
    Accomodation.objects.all().delete()
    Cafe.objects.all().delete()
    Place.objects.all().delete()
    Medical.objects.all().delete()

    c = open("./static/csv/cafe.csv",'r',encoding='CP949')
    a = open("./static/csv/accommo.csv",'r',encoding='CP949')
    p = open("./static/csv/place.csv",'r',encoding='CP949')
    m = open("./static/csv/medical.csv",'r',encoding='CP949')
    
    reader_cafe = csv.reader(c)
    reader_accomo = csv.reader(a)
    reader_place = csv.reader(p)
    reader_medical = csv.reader(m)

    cafes = []
    places = []
    accomos = []
    medicals = []

    for row in reader_accomo:
        accomos.append(Accomodation(name=row[0],location=row[1],address=row[2],phone=row[3],type=row[4],link1=row[5],desc=row[6],img=row[7],x=row[8],y=row[9]))
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

    for r in reader_medical:
        try:
            medicals.append(Medical(name=r[0],location=r[1],phone=r[2],address=r[3],doro=r[4],hourInfo=r[5],x=r[6],y=r[7],distance=0, link=r[8]))
        except:
            medicals.append(Medical(name=r[0],location=r[1],phone=r[2],address=r[3],doro=r[4],hourInfo='',x=r[6],y=r[7],distance=0, link=r[8]))
    Medical.objects.bulk_create(medicals)

    c.close()
    a.close()
    p.close()
    m.close()

    return HttpResponse('create model~')

    ##### 멍초이스 작성

# def create(request, category, categry_id):
#     current_user = request.user # 현재 접속한 user를 가져온다.
#     me = User.objects.get(username=current_user) # User db에서 현재 접속한 user를 찾는다.
    
#     if category == "cafe":
#         post = Cafe.objects.get(id=categry_id)
#     if category == "accommo":
#         post = Accomodation.objects.get(id=categry_id)
#     if category == "place":
#         post = Place.objects.get(id=categry_id)

#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post=form.save()
#             post.update(user=me.id, postType=category,placeId=categry_id)
#             post.save()

#             return redirect('/${category}/${categry_id}')
#     else:
#         form=PostForm()
#     return render(request, 'reviewWrite.html', {'form':form , 'post':post})

def create(request,category,category_id):
    current_user = request.user # 현재 접속한 user를 가져온다.
    me = User.objects.get(username=current_user) # User db에서 현재 접속한 user를 찾는다.

    if category == 'cafe':
        place = Cafe.objects.get(id=category_id)
    elif category == 'accomo':
        place = Accomodation.objects.get(id=category_id)
    else:
        place = Place.objects.get(id=category_id)

    placeName = place.name
    location=place.location

    if request.method == "POST":
        postGood = request.POST["postGood"]
        postBad = request.POST["postBad"]
        postImage = request.FILES['postImage']
        ranking = request.POST["ranking"]
        new_post=Post.objects.create(user=me,postType=category,postImage=postImage,postGood=postGood,postBad=postBad,ranking=ranking, placeId=category_id)

        return redirect(f"/reviewDetail/{new_post.id}")
    else:
        return render(request, 'reviewWrite.html', {'placeName':placeName,'location':location, 'category':category, 'category_id':category_id})

        

@csrf_exempt
def like(request):
    req = json.loads(request.body)
    category = req['category']
    place_id = req['place_id']

    try:
        current_user = request.user # 현재 접속한 user를 가져온다.
        me = User.objects.get(username=current_user) # User db에서 현재 접속한 user를 찾는다.
        isLogin = True
        try:
            like = Like.objects.get(Q(user=me) & Q(placeType=category) & Q(placeId=place_id))
        except:
            Like.objects.create(user=me, placeType=category, placeId=place_id) # 없으면 만들어주라

        like = Like.objects.get(Q(user=me) & Q(placeType=category) & Q(placeId=place_id))
        if like.like == True:
            like.like = False
            like.save()
        elif like.like == False:
            like.like = True
            like.save()
    except:
        isLogin = False

    return JsonResponse({ 'place_id':place_id, 'isLogin':isLogin })

def reviewDetail(request, id):
    review = Post.objects.get(id=id)
    category = review.postType

    if category == 'cafe':
        place = Cafe.objects.get(id=review.placeId)
    elif category == 'place':
        place = Place.objects.get(id=review.placeId)
    else:
        place = Accomodation.objects.get(id=review.placeId)
    
    context = {'review':review, 'place':place}

    return render(request, 'reviewDetail.html', context=context)

def mypage(request):
    current_user = request.user # 현재 접속한 user를 가져온다.
    me = User.objects.get(username=current_user) # User db에서 현재 접속한 user를 찾는다.

    likePlaces = []
    
    try:
        likes = Like.objects.filter(Q(user=me) & Q(like=True))

        for like in likes:
            if like.placeType == 'cafe':
                place = Cafe.objects.get(id=like.placeId)
            elif like.placeType == 'place':
                place = Place.objects.get(id=like.placeId)
            else:
                place = Accomodation.objects.get(id=like.placeId)
            likePlaces.append(place)
    except:
        likePlaces = []

    posts = Post.objects.filter(user=me)

    context = {'posts':posts, 'likePlaces':likePlaces}

    return render(request, 'mypage.html', context=context)

import requests
def medicalSearch(searching):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
    headers = {
    "Authorization": "KakaoAK fbbcd36dba0d5dd1d57a28b0a17b614b"
    }
    result = requests.get(url, headers = headers).json()['documents']
    resultX = result[0]['x']
    resultY = result[0]['y']
    return resultX, resultY

import math
def distance(x1, y1, x2, y2):
    result = abs(float(x1) - float(x2)) + abs(float(y1) - float(y2))
    return result

def map(request):

    return render(request, 'maps.html')