from django.conf.urls import url
from django.contrib import admin
from MLWebService import views
 
urlpatterns = [
    url(r'^index', views.upload,name="upload"),
    url(r'^uploaded',views.uploaded,name="uploaded"),
]