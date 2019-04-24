from django.conf.urls import url
from django.contrib import admin
from MLWebService import views
 
urlpatterns = [
    url(r'^upload', views.upload,name="upload"),
    url(r'^tasks',views.showTasks,name="tasks"),
    url(r'^task(\d+)',views.startTrainModel,name="train"),
    url(r'^dataframe(\d+)',views.dataFrame,name="data"),
    url(r'^test(\d+)',views.showTest,name="tests"),
    url(r'^startTest(\d+)',views.startTest,name="test"),
    url(r'^login',views.login,name="login"),
    url(r'^register', views.register),
    url(r'^logout', views.logout),
    url(r'',views.index, name = 'index'),
]