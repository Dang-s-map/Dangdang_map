from asyncio.windows_events import NULL
from dis import dis
import email
from http.client import HTTPResponse
from imaplib import _Authenticator
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
from django.contrib.auth import authenticate
# Create your views here.


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("username : ", username)
        print("password : ", password)
        user = User.objects.create_user( username="whatever3", email="whatever@some.com", password="password")
        user.save()
        user = authenticate( username="whatever3",password="password")
        

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
    place_set =[]
    reviews = []
    places = []
    counts = []
    categoryList = ['cafe', 'place', 'accomo']

    for category in categoryList:
        try:
            place_ides = list(set(Post.objects.filter(postType=category).values_list('placeId', flat=True)))
            place_id = random.choice(place_ides)
            place_set.append([category, place_id])
        except: #해당 카테고리에 리뷰가 없을 경우
            pass
    for p in place_set:
        try:
            if p[0] == 'cafe':
                posts = Post.objects.filter(Q(postType='cafe') & Q(placeId=p[1]))
                random_id = random.choice(posts).id
                post = Post.objects.get(id=random_id)
                place = Cafe.objects.get(id=p[1])
            elif p[0] == 'place':
                posts = Post.objects.filter(Q(postType='place') & Q(placeId=p[1]))
                random_id = random.choice(posts).id
                post = Post.objects.get(id=random_id)
                place = Place.objects.get(id=p[1])
            elif p[0] == 'accomo':
                posts = Post.objects.filter(Q(postType='accomo') & Q(placeId=p[1]))
                random_id = random.choice(posts).id
                post = Post.objects.get(id=random_id)
                place = Accomodation.objects.get(id=p[1])
            reviews.append(post)
            places.append(place)
            place_review = Post.objects.filter(placeId=place.id)
            counts.append(len(place_review))
        except: #해당 카테고리에 리뷰가 없을 경우
            pass
    total_list=zip(reviews,places,counts)

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
        
        filteredLocation = filteredLocation.order_by('id') # 아이디순으로 정렬
        paginator = Paginator(filteredLocation, 5)   
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        context = {'category': category ,'location': location,'locations': locations, 'type': type,'posts': posts }
        return render(request, 'mainList.html', context=context)


### 사이트에서 이미지 불러오기

############ 네이버 쳤을 때 창
def page1(place):
  
  cookies = {
      'NNB': 'G5AA6C3FLZ4V2',
      'ASID': 'dbffcf840000016e3a5eee630000004a',
      'NFS': '2',
      '_ga_7VKFYR6RV1': 'GS1.1.1597901340.14.1.1597901683.46',
      'm_loc': 'd5fae313eb8f8d9c7050efd25232798d9d46bed2a51ca5b050c23aad802b4a881dfb12bada235ad6a69a9ce7f073c11ed5ec98ec7cfd21f8212a26f84dad9d5d',
      'NV_WETR_LOCATION_RGN_M': '"MDMyMjAxMTE="',
      'NV_WETR_LAST_ACCESS_RGN_M': '"MDMyMjAxMTE="',
      '_fbp': 'fb.1.1652333053952.1864013727',
      '_gcl_au': '1.1.924982538.1652333054',
      '_ga_1BVHGNLQKG': 'GS1.1.1653819791.2.1.1653819793.0',
      '_ga': 'GA1.2.1918082713.1576255170',
      '_ga_4BKHBFKFK0': 'GS1.1.1657104703.4.1.1657105489.0',
      'nx_ssl': '2',
      'csrf_token': 'c9ff8dc89d0d26f7321703f51cfc2d4448818847853c526728a4d2219155c97e9b6490d088524f5e2d1f9fdd189f23d95bdd86f6e9ca8c8b07bf30c857e040c6',
      'nid_inf': '1648409857',
      'NID_JKL': 'k/RAiTYAFS6RkhgqnogzAaXMauAE19RkQbwr15wgb58=',
      'BMR': 's=1659778687634&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Denglishtoto1%26logNo%3D220309727641&r2=https%3A%2F%2Fwww.google.com%2F',
      'page_uid': 'aa030e03-045c-47e7-b1cb-e53cf84aa4ee',
      '_naver_usersession_': 'mSmf4dxGzWxu2j4wJ8Rr8A==',
      'page_uid': 'hYtT8lp0J1Zssbe79xwsssssttl-328898',
  }

  headers = {
      'authority': 'map.naver.com',
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
      'cache-control': 'no-cache',
      'content-type': 'application/json',
      # Requests sorts cookies= alphabetically
      # 'cookie': 'NNB=G5AA6C3FLZ4V2; ASID=dbffcf840000016e3a5eee630000004a; NFS=2; _ga_7VKFYR6RV1=GS1.1.1597901340.14.1.1597901683.46; m_loc=d5fae313eb8f8d9c7050efd25232798d9d46bed2a51ca5b050c23aad802b4a881dfb12bada235ad6a69a9ce7f073c11ed5ec98ec7cfd21f8212a26f84dad9d5d; NV_WETR_LOCATION_RGN_M="MDMyMjAxMTE="; NV_WETR_LAST_ACCESS_RGN_M="MDMyMjAxMTE="; _fbp=fb.1.1652333053952.1864013727; _gcl_au=1.1.924982538.1652333054; _ga_1BVHGNLQKG=GS1.1.1653819791.2.1.1653819793.0; _ga=GA1.2.1918082713.1576255170; _ga_4BKHBFKFK0=GS1.1.1657104703.4.1.1657105489.0; nx_ssl=2; csrf_token=c9ff8dc89d0d26f7321703f51cfc2d4448818847853c526728a4d2219155c97e9b6490d088524f5e2d1f9fdd189f23d95bdd86f6e9ca8c8b07bf30c857e040c6; nid_inf=1648409857; NID_JKL=k/RAiTYAFS6RkhgqnogzAaXMauAE19RkQbwr15wgb58=; BMR=s=1659778687634&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Denglishtoto1%26logNo%3D220309727641&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=aa030e03-045c-47e7-b1cb-e53cf84aa4ee; _naver_usersession_=mSmf4dxGzWxu2j4wJ8Rr8A==; page_uid=hYtT8lp0J1Zssbe79xwsssssttl-328898',
      'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
      'pragma': 'no-cache',
      'referer': 'https://map.naver.com/',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  }

  global response1
  response1 = requests.get('https://map.naver.com/v5/api/search?caller=pcweb&query='+place+'&type=all&searchCoord=128.91334039999987;37.78818840000017&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko', cookies=cookies, headers=headers)

############################각 장소의 상세페이지
import requests

def page2(id):
  cookies = {
    'NNB': 'G5AA6C3FLZ4V2',
    'ASID': 'dbffcf840000016e3a5eee630000004a',
    'NFS': '2',
    '_ga_7VKFYR6RV1': 'GS1.1.1597901340.14.1.1597901683.46',
    'm_loc': 'd5fae313eb8f8d9c7050efd25232798d9d46bed2a51ca5b050c23aad802b4a881dfb12bada235ad6a69a9ce7f073c11ed5ec98ec7cfd21f8212a26f84dad9d5d',
    'NV_WETR_LOCATION_RGN_M': '"MDMyMjAxMTE="',
    'NV_WETR_LAST_ACCESS_RGN_M': '"MDMyMjAxMTE="',
    '_fbp': 'fb.1.1652333053952.1864013727',
    '_gcl_au': '1.1.924982538.1652333054',
    '_ga_1BVHGNLQKG': 'GS1.1.1653819791.2.1.1653819793.0',
    '_ga': 'GA1.2.1918082713.1576255170',
    '_ga_4BKHBFKFK0': 'GS1.1.1657104703.4.1.1657105489.0',
    'nx_ssl': '2',
    'csrf_token': 'c9ff8dc89d0d26f7321703f51cfc2d4448818847853c526728a4d2219155c97e9b6490d088524f5e2d1f9fdd189f23d95bdd86f6e9ca8c8b07bf30c857e040c6',
    'nid_inf': '1648409857',
    'NID_JKL': 'k/RAiTYAFS6RkhgqnogzAaXMauAE19RkQbwr15wgb58=',
    'BMR': 's=1659778687634&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Denglishtoto1%26logNo%3D220309727641&r2=https%3A%2F%2Fwww.google.com%2F',
    'page_uid': 'hYtT8lp0J1Zssbe79xwsssssttl-328898',
    'page_uid': '129552a0-b083-42e7-8d1e-85eeae8b8e99',
}

  headers = {
    'authority': 'map.naver.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'NNB=G5AA6C3FLZ4V2; ASID=dbffcf840000016e3a5eee630000004a; NFS=2; _ga_7VKFYR6RV1=GS1.1.1597901340.14.1.1597901683.46; m_loc=d5fae313eb8f8d9c7050efd25232798d9d46bed2a51ca5b050c23aad802b4a881dfb12bada235ad6a69a9ce7f073c11ed5ec98ec7cfd21f8212a26f84dad9d5d; NV_WETR_LOCATION_RGN_M="MDMyMjAxMTE="; NV_WETR_LAST_ACCESS_RGN_M="MDMyMjAxMTE="; _fbp=fb.1.1652333053952.1864013727; _gcl_au=1.1.924982538.1652333054; _ga_1BVHGNLQKG=GS1.1.1653819791.2.1.1653819793.0; _ga=GA1.2.1918082713.1576255170; _ga_4BKHBFKFK0=GS1.1.1657104703.4.1.1657105489.0; nx_ssl=2; csrf_token=c9ff8dc89d0d26f7321703f51cfc2d4448818847853c526728a4d2219155c97e9b6490d088524f5e2d1f9fdd189f23d95bdd86f6e9ca8c8b07bf30c857e040c6; nid_inf=1648409857; NID_JKL=k/RAiTYAFS6RkhgqnogzAaXMauAE19RkQbwr15wgb58=; BMR=s=1659778687634&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Denglishtoto1%26logNo%3D220309727641&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hYtT8lp0J1Zssbe79xwsssssttl-328898; page_uid=129552a0-b083-42e7-8d1e-85eeae8b8e99',
    'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
    'pragma': 'no-cache',
    'referer': 'https://map.naver.com/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

  params = {
    'lang': 'ko',
}
  global response2
  response2 = requests.get('https://map.naver.com/v5/api/sites/summary/'+id, params=params, cookies=cookies, headers=headers)

#############################################


## mainList 목록눌렀을때 상세페이지로 이동 (listDetail.html)
def listDetail(request, category, id):
    if category == 'cafe':
        here = Cafe.objects.get(id=id)
    elif category == 'place':
        here = Place.objects.get(id=id)
    elif category == 'accomo':
        here = Accomodation.objects.get(id=id)


    try:
        reviews = Post.objects.filter(Q(postType=category)&Q(placeId=id))
    except:
        reviews = '아직 리뷰가 없습니다.'
        pass

    # 이미지 크롤링
    photo_list=[]

    place = here.location + ' ' + here.name 
    page1(place)
  
    try:
        dict=response1.json()
        dict_prepare = dict['result']['place']['list'][0]
        id=dict_prepare['id']

        page2(id)
        dict2=response2.json()
        i=1
        for photo in dict2['images']:
            photo_list.append(photo['url'])
            if i>9 :
                break
            i+=1

    except:
        photo_list=[] 

    context = {'category': category ,'here': here, 'reviews': reviews, 'photos' : photo_list}
    return render(request, 'listDetail.html', context=context)

def medicalList(request): # main에서 응급댕댕 선택시
    places = Medical.objects.filter(location='강원')[:10]
    context = { 'places':places }
    return render(request, 'medicalList.html', context=context)

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

## 멍초이스 (post) 부분

def delete(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)

        category = post.postType
        place_id = post.placeId

        if category == 'cafe':
            place = Cafe.objects.get(id=place_id)
        elif category == 'accomo':
            place = Accomodation.objects.get(id=place_id)
        else:
            place = Place.objects.get(id=place_id)
        
        post.delete()

        # 별점저장
        posts = Post.objects.filter(Q(postType=category)&Q(placeId=place_id))
        total = 0
        len_posts= len(posts)
        for p in posts:
            total += p.ranking
        if len_posts == 0:
            place.star = 0
        else:
            place.star = total/len_posts
        place.save()
        return redirect("/") # 삭제하고 나면 어디로 보낼까요?
    
    

def update(request, id): 
    post = Post.objects.get(id=id)
    category = post.postType
    placeId = post.placeId
    
    if category == 'cafe':
        place = Cafe.objects.get(id=placeId)
    elif category == 'accomo':
        place = Accomodation.objects.get(id=placeId)
    else:
        place = Place.objects.get(id=placeId)

    placeName = place.name
    location=place.location
    if request.method == "POST":
                postGood = request.POST["postGood"]
                postBad = request.POST["postBad"]
                try:
                    postImage = request.FILES.get["postImage"]
                except:
                    pass

                ranking = request.POST["ranking"]

                try:
                    Post.objects.filter(id=id).update(postGood=postGood,postBad=postBad,postImage=postImage,ranking=ranking)
                    posts = Post.objects.filter(Q(postType=category)&Q(placeId=placeId))
                    total = 0
                    len_posts= len(posts)
                    for p in posts:
                        total += p.ranking
                    place.star = total/len_posts
                    place.save()
                except:
                    Post.objects.filter(id=id).update(postGood=postGood,postBad=postBad,ranking=ranking)
                    posts = Post.objects.filter(Q(postType=category)&Q(placeId=placeId))
                    total = 0
                    len_posts= len(posts)
                    for p in posts:
                        total += p.ranking
                    place.star = total/len_posts
                    place.save()
                return redirect(f"/reviewDetail/{post.id}")

            
    else:
                
                context = {"post":post, "placeName":placeName, "category":category, 'location':location}
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
        accomos.append(Accomodation(name=row[0],location=row[1],address=row[2],phone=row[3],type=row[4],link=row[5],desc=row[6],img=row[7],x=row[8],y=row[9],reserveLink=row[10]))
    Accomodation.objects.bulk_create(accomos)

    for r in reader_cafe:
        try:
            cafes.append(Cafe(name=r[0],location=r[1],address=r[2],phone=r[3],type=r[4],menuInfo=r[5],hourInfo=r[6],link=r[7],desc=r[8],img=r[9],x=r[10],y=r[11]))
        except:
            cafes.append(Cafe(name=r[0],location=r[1],address=r[2],phone=r[3],type=r[4],menuInfo=r[5],hourInfo=r[6],link=r[7],desc=r[8],img=r[9]))
    Cafe.objects.bulk_create(cafes)

    for r in reader_place:
        places.append(Place(name=r[0],location=r[1],address=r[2],phone=r[3],type=r[4],link=r[6],desc=r[7],img=r[8],x=r[9],y=r[10]))
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
        try:
            postImage = request.FILES.get["postImage"]
        except:
            pass

        ranking = request.POST["ranking"]
        try:
            new_post=Post.objects.create(user=me,postType=category,postImage=postImage,postGood=postGood,postBad=postBad,ranking=ranking, placeId=category_id)
            posts = Post.objects.filter(Q(postType=category)&Q(placeId=category_id))
            total = 0
            len_posts= len(posts)
            for p in posts:
                total += p.ranking
            place.star = total/len_posts
            place.save()
        except:
            new_post=Post.objects.create(user=me,postType=category,postGood=postGood,postBad=postBad,ranking=ranking, placeId=category_id)
            posts = Post.objects.filter(Q(postType=category)&Q(placeId=category_id))
            total = 0
            len_posts= len(posts)
            for p in posts:
                total += p.ranking
            place.star = total/len_posts
            place.save()

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
    
    context = {'review':review, 'place':place, 'category':category,}

    return render(request, 'reviewDetail.html', context=context)

def mypage(request):
    current_user = request.user # 현재 접속한 user를 가져온다.
    me = User.objects.get(username=current_user) # User db에서 현재 접속한 user를 찾는다.

    likePlaces = []
    category = []
    postPlaces = []
    
    try:
        likes = Like.objects.filter(Q(user=me) & Q(like=True))

        for like in likes:
            if like.placeType == 'cafe':
                place = Cafe.objects.get(id=like.placeId)
                category.append('cafe')
            elif like.placeType == 'place':
                place = Place.objects.get(id=like.placeId)
                category.append('place')
            else:
                place = Accomodation.objects.get(id=like.placeId)
                category.append('accomo')
            likePlaces.append(place)
        total_like=zip(category,likePlaces)

    except:
        likePlaces = []

    posts = Post.objects.filter(user=me)
    for post in posts:
        if post.postType == 'cafe':
            place = Cafe.objects.get(id=post.placeId)
        elif post.postType == 'place':
            place = Place.objects.get(id=post.placeId)
        else:
            place = Accomodation.objects.get(id=post.placeId)
        postPlaces.append(place)
    total_post=zip(posts,postPlaces)
        
    context = {'total_post':total_post, 'total_like':total_like}

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

## review 저장
def reviewToModel(request):
    Post.objects.all().delete()
    tempUser = User.objects.create(username='naver&google',password='asdf1234',email='abcd@google.com')

    r = open("./static/csv/review.csv",'r',encoding='utf-8')
    reader_review = csv.reader(r)

    reviews = []

    for row in reader_review:
        if row[2] == 'cafe':
            try:
                info = Cafe.objects.filter(Q(name=row[0])&Q(location=row[1]))[0]
                try:
                    if row[3] and row[4]:
                        reviews.append(Post(postType='cafe',postImage=row[5],postGood=row[4],postBad='',ranking=float(row[3]),placeId=info.id,user=tempUser))
                        Cafe.objects.filter(id=info.id).update(star=float(row[3]))
                    elif not row[3]:
                        reviews.append(Post(postType='cafe',postImage=row[5],postGood=row[4],postBad='',ranking=0,placeId=info.id,user=tempUser))
                        Cafe.objects.filter(id=info.id).update(star=float(0))
                    elif not row[4]:
                        reviews.append(Post(postType='cafe',postImage=row[5],postGood='',postBad='',ranking=float(row[3]),placeId=info.id,user=tempUser))
                        Cafe.objects.filter(id=info.id).update(star=float(row[3]))
                except:
                    continue
            except:
                continue
        elif row[2]  == 'place':
            try:
                info = Place.objects.filter(Q(name=row[0])&Q(location=row[1]))[0]
                try:
                    if row[3] and row[4]:
                        reviews.append(Post(postType='place',postImage=row[5],postGood=row[4],postBad='',ranking=float(row[3]),placeId=info.id,user=tempUser))
                        Place.objects.filter(id=info.id).update(star=float(row[3]))
                    elif not row[3]:
                        reviews.append(Post(postType='place',postImage=row[5],postGood=row[4],postBad='',ranking=0,placeId=info.id,user=tempUser))
                        Place.objects.filter(id=info.id).update(star=float(0))
                    elif not row[4]:
                        reviews.append(Post(postType='place',postImage=row[5],postGood='',postBad='',ranking=float(row[3]),placeId=info.id,user=tempUser))
                        Place.objects.filter(id=info.id).update(star=float(row[3]))
                except:
                    continue
            except:
                continue
        else:
            try:
                info = Accomodation.objects.filter(Q(name=row[0])&Q(location=row[1]))[0]
                try:
                    if row[3] and row[4]:
                        reviews.append(Post(postType='accomo',postImage=row[5],postGood=row[4],postBad='',ranking=float(row[3]),placeId=info.id,user=tempUser))
                        Accomodation.objects.filter(id=info.id).update(star=float(row[3]))
                    elif not row[3]:
                        reviews.append(Post(postType='accomo',postImage=row[5],postGood=row[4],postBad='',ranking=0,placeId=info.id,user=tempUser))
                        Accomodation.objects.filter(id=info.id).update(star=float(0))
                    elif not row[4]:
                        reviews.append(Post(postType='accomo',postImage=row[5],postGood='',postBad='',ranking=float(row[3]),placeId=info.id,user=tempUser))
                        Accomodation.objects.filter(id=info.id).update(star=float(row[3]))
                except:
                    continue
            except:
                continue
    Post.objects.bulk_create(reviews)

    r.close()
    return HttpResponse('create review~')
