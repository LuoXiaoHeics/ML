from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.forms import fields
from django import forms
from MLWebService.models import trainingTask
from MLWebService.learning import learnThread
import threading
import os
# Create your views here.
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        trainingData = request.FILES.get('trainingData')
        modelName_m = request.POST.get('modelName')
        type_m = request.POST.get('modelSelection')
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fileName = os.path.join(PROJECT_ROOT,'MLWebService\data',trainingData.name)
        f = open(fileName,'wb')
        for line in trainingData.readlines():
            f.write(line)
        f.close()
        onTraining_m = -1
        newTraining = trainingTask(trainingName=modelName_m, trainingDataFile = fileName,\
                typeOfModel = type_m,onTraining = -1)
        newTraining.save()
        return HttpResponseRedirect(reverse("uploaded"))
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates','index.html'))

@csrf_exempt
def welcome(request):
    return HttpResponse("<h1>Welcome to Machine Learning training platform</h1>")

def uploaded(request):
    return HttpResponse("<h1>file uploaded</h1>")

def startTrainModel(request,oid):
    if request.method=="POST":
        waitTraining =trainingTask.objects().filter(onTraining=-1)
        #训练模型
        return HttpResponse("<h1>Start to Train"+ oid+"</h1>") #返回一个reverse
    return HttpResponse("error")

def showTasks(request):
    print(request.POST)
    onTrainingModel = trainingTask.objects.filter(onTraining=0)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_list = os.listdir(os.path.join(PROJECT_ROOT,'MLWebService/CompleteModels'))
    for mod in onTrainingModel:
        if mod.trainingName+".pickle" in dir_list:
            mod.onTraining=1
            mod.save()
        else:continue
    results = trainingTask.objects.all()
    return  render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates/tasks.html'),{"data": results.all()})

def test(request,oid):
      return HttpResponse("<h1>Welcome to test"+ oid)
#render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates/test.html'))  