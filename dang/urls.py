from django.urls import path 

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "dang"

urlpatterns = [

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)