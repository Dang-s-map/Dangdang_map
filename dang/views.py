from asyncio.windows_events import NULL
from http.client import HTTPResponse
from re import template
from unicodedata import category
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.db.models import Q
import csv
from .models import Favorite, User, Post, Cafe, Place, Accomodation, Medical
from django.core.paginator import Paginator
from .forms import PostForm


from django.core import serializers
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email.policy import default
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.


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

# nav바에서 카테고리 눌렀을 때
def navToList(request, category, location, type):
    filteredLocation = 'nothing_yet'
    if category == 'cafe':
        filteredLocation=Cafe.objects.filter(Q(location=location)&Q(type=type))
    elif category == 'place':
        filteredLocation=Place.objects.filter(Q(location=location)&Q(type=type))
    elif category == 'accomo':
        filteredLocation=Accomodation.objects.filter(Q(location=location)&Q(type=type))
    try:
        paginator = Paginator(filteredLocation, 5)
    except:
        pass
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {'category': category ,'posts': posts}
    return render(request, 'mainList.html', context=context)

## mainList 목록눌렀을때 상세페이지로 이동 (listDetail.html)
def listDetail(request, category, id):
    if category == 'cafe':
        here = Cafe.objects.get(id=id)
    elif category == 'place':
        here = Place.objects.get(id=id)
    elif category == 'accomo':
        here = Accomodation.objects.get(id=id)
    context = {'category': category ,'here': here}
    return render(request, 'listDetail.html', context=context)

def mainList(request, location): # main에서 지역 선택했을 때
    only_loc= Cafe.objects.filter(Q(location=location)& Q(type='애견동반'))
    category = 'cafe'
    context = { "location" : location, 'list' : only_loc ,'category':category}
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
    

# def cafeDetail(request, id):
#     cafe = Cafe.objects.get(id=id)
#     reviews = cafe.cafe_post.all() # 역참조한건데 제대로 되나 test 해봐야 함
#     category = 'cafe'
#     context = { "cafe":cafe, "reviews":reviews, "id":id, "category":category }
#     return render(request, 'cafeDetail.html', context=context)
    


## 멍초이스 (post) 부분

def delete(request, id):
    Post.objects.filter(id=id).delete()
    return redirect("/") # 삭제하고 나면 어디로 보낼까요?

def update(request, id): # url수정하기
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post=form.save()
            post.save()
        
            # if 문으로 어떤 카테고리인지 체크 -> cafe라면 accomo, place는 null 값이기 때문에
            if post.cafe:
                cate = 'cafe'
            elif post.place:
                cate = 'place'
            elif post.accomo:
                cate = 'accomo'

            return redirect(f"/post/{cate}/{id}")
    form = PostForm(instance=post)
    return render(request, "무슨무슨.html", {'form':form})


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
    if category == "cafe":
        post = Cafe.objects.get(id=categry_id)
    if category == "accommo":
        post = Accomodation.objects.get(id=categry_id)
    if category == "place":
        post = Place.objects.get(id=categry_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save()
            post.save()
            return redirect('/${category}/${categry_id}')
    else:
        form=PostForm()
    return render(request, 'reviewWrite.html', {'form':form , 'post':post})



@csrf_exempt
def like(request):
    req = json.loads(request.body)
    fav_id = req['id']
    favorite = Favorite.objects.get(id=fav_id)
    if favorite.like == True:
        favorite.like = False
        favorite.like = True
    elif favorite.like == False:
        favorite.save()
    return JsonResponse({'id':fav_id, 'type' : favorite.like})

def reviewDetail(request, id):
    review = Post.objects.get(id=id)

    if review.cafe_post: # 역참조 test 해봐야 함. 안 될 수도
        placeInfo = review.cafe_post.all()
    elif review.place_post:
        placeInfo = review.place_post.all()
    elif review.accomo_post:
        placeInfo = review.accomo_post.all()
    
    context = {'review':review, 'place':placeInfo}

    return render(request, 'reviewDetail.html', context=context)



