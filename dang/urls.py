from django.contrib import admin
from django.urls import path 

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "dang"

urlpatterns = [
  path('', views.home, name='home'),
  path('cafe', views.cafeList, name='cafeList'),
  path('place', views.placeList, name='placeList'),
  path('accomo', views.accomoList, name='accomoList'),
  path('medical', views.medicalList, name='medicalList'),
  path('cates/', views.cates, name='cates'), # category 선택 ajax
  path('locationBtn/', views.locationBtn, name='locationBtn'), # 지역 고르기 ajax
  path('listGo/', views.listGo, name='listGo'), # 선택 적용 ajax
  path('cities/<str:location>', views.mainList, name='mainList'),
  path('csvToModel', views.csvToModel, name='csvToModel'), # db 설정용 url
  path('cafe/<int:id>', views.cafeDetail, name='cafeDetail'), # 상세페이지(카페)
  path('accommo/<int:id>', views.accommoDetail, name='accommoDetail'), # 상세페이지(카페)
  path('place/<int:id>', views.placeDetail, name='placeDetail'), # 상세페이지(카페)
  path('', views.home, name='home'),
  path('admin/', admin.site.urls),
  path('login/', views.login, name='login'),
  path('join/', views.join, name='join'),
  path('logout/', views.logout, name='logout'),
  path('mypage/', views.mypage, name='mypage'),
  path('create/<str:category>/<int:id>', views.create, name='create'),  # 멍초이스 작성페이지
  # 여기서 id = {{cafe.id}} 처럼 카테고리.id 임.
  # category 는 Cafe,Accomodation, Place 들 중 하나로 넘겨줘

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
