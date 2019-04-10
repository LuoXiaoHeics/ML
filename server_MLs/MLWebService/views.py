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
        print("目前的线程数为：%d" %threading.active_count())
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

def startTrainModel(request):
    if request.method=="POST":
        waitTraining =trainingTask.objects().filter(onTraining="-1")

def showTasks(request):
    results = trainingTask.objects.all()
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return  render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates/tasks.html'),{"data": results.all()})
