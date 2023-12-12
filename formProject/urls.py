"""
URL configuration for formProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from formapp.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',anasayfa),
    path('register/',register,name="register"),
    path('login/',giris,name="giris"),
    path('exit',exit,name="exit"),
    path('form/ekle',notEkle,name='ekle'),
    path('hata',hata,name='hata'),
    path('detail/<formid>',notDetail,name='detay'),
    path('myforms',myForms,name='forms'),
    path('detail/delete/<formid>',delete,name='delete'),
    path('detail/update/<formid>',update,name='update'),
    #profil sayfası
    path('profile/<userid>',profile,name='profil')    ,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)