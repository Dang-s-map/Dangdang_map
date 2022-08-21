from django.contrib import admin
from django.urls import path, include 

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "dang"

urlpatterns = [
  path('', views.home, name='home'),
  path('list/<str:category>/<str:location>/<str:type>', views.toMainList, name='toMainList'), # 메인 -> (nav) 카테고리
  path('medical/list', views.medicalList, name='medicalList'), # 메인 -> (nav) 응급댕댕
  path('cates/', views.cates, name='cates'), # category 선택 ajax
  path('csvToModel', views.csvToModel, name='csvToModel'), # db 설정용 url
  path('reviewToModel', views.reviewToModel, name='reviewToModel'), # db 설정용 url
  path('detail/<str:category>/<int:id>', views.listDetail, name='listDetail'), #목록상세페이지
  path('login/', views.login, name='login'),
  path('join/', views.join, name='join'),
  path('logout', views.logout, name='logout'),
  path('mypage/', views.mypage, name='mypage'),
  path('like/', views.like, name='like'),
  path('btn_main/', views.btn_main, name='btn_main'), #ajax - 어디로 떠날까요, mainList-btn
  path('create/<str:category>/<int:category_id>', views.create, name='create'),  # 멍초이스 작성페이지
  path('delete/<int:id>', views.delete, name="delete"), # post 삭제
  path('update/<int:id>', views.update, name="update"), # post 수정
  path('reviewDetail/<int:id>', views.reviewDetail, name='reviewDetail'), # 리뷰 디테일로 넘어간다.
  path('accounts/', include('allauth.urls')),
  path('medicals/', views.medicals, name='medicals'), # medical ajax
  
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


