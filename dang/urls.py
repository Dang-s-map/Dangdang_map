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
  path('accommo/<int:id>', views.accommoDetail, name='accommoDetail'), # 상세페이지(숙소)
  path('place/<int:id>', views.placeDetail, name='placeDetail'), # 상세페이지(장소)
  path('', views.home, name='home'),
  path('admin/', admin.site.urls),
  path('login/', views.login, name='login'),
  path('join/', views.join, name='join'),
  path('logout', views.logout, name='logout'),
  path('mypage/', views.mypage, name='mypage'),
  path('detail', views.detail, name='detail'),
  path('like/', views.like, name='like'),
  path('btn_left/', views.btn_left, name='btn_left'), #ajax - 어디로 떠날까요
  path('btn_right/', views.btn_right, name='btn_right'), # ajax - 어디로 떠날까요
  path('create/<str:category>/<int:id>', views.create, name='create'),  # 멍초이스 작성페이지
  path('delete/<int:id>', views.delete, name="delete"), # post 삭제
  path('update/<int:id>', views.update, name="update"), # post 수정
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


