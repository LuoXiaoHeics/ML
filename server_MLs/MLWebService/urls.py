from django.conf.urls import url
from django.contrib import admin
from MLWebService import views
 
urlpatterns = [
    url(r'^index', views.upload,name="upload"),
    url(r'^uploaded',views.uploaded,name="uploaded"),
    url(r'^tasks',views.showTasks,name="tasks"),
    url(r'^task(\d+)',views.startTrainModel,name="train"),
    url(r'^test(\d+)',views.showTest,name="tests"),
    url(r'^startTest(\d+)',views.startTest,name="test"),
]