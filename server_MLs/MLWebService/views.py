from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.forms import fields
from django import forms
from server_MLs.settings import logging
from MLWebService.models import trainingTask
from MLWebService.models import MLUser
from MLWebService.learning import learnThread
import threading
import os
from sklearn.externals import joblib
import time
import datetime
import numpy as np
from .forms import *

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = MLUser.objects.filter(username=username)
                if user[0].password == password:             
                    request.session['is_login'] = True
                    request.session['user_name'] = username
                    return HttpResponseRedirect(reverse("index"))
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, os.path.join(PROJECT_ROOT,'MLWebService/templates','login.html'), locals())
    login_form = UserForm()
    return render(request, os.path.join(PROJECT_ROOT,'MLWebService/templates','login.html'), locals())

def index(request):
    if  not request.session.get('is_login', None):
        havelogin = False
    else : havelogin = True
     #if request.method == "POST":
     #   username = request.POST.get('username')
     #   password = request.POST.get('password')
    print (havelogin)
    return render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates','index.html'),locals())

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        message = "请检查填写的内容！"
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        anwser = request.POST.get('question')
        if (username!="") and (password!="") and (anwser =="LuoXiaoHei"):
            user = MLUser.objects.filter(username=username)
            if len(user) >0:             
                message = "用户名已存在"
            else:
                newUser = MLUser(username=username,password=password,email=email)
                newUser.save()
                return HttpResponseRedirect(reverse("login"))
        else: message = "信息错误"
        return render(request, os.path.join(PROJECT_ROOT,'MLWebService/templates','register.html'), locals())
    return render(request, os.path.join(PROJECT_ROOT,'MLWebService/templates','register.html'))
    

def upload(request):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        trainingData = request.FILES.get('trainingData')
        modelName_m = request.POST.get('modelName')
        type_m = request.POST.get('modelSelection')
        fileName = os.path.join(PROJECT_ROOT,'MLWebService\data',trainingData.name)
        f = open(fileName,'wb')
        for line in trainingData.readlines():
            f.write(line)
        f.close()
        onTraining_m = -1
        newTraining = trainingTask(trainingName=modelName_m, trainingDataFile = fileName,\
                typeOfModel = type_m,onTraining = -1)
        newTraining.save()
        return render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates','uploaded.html'))
    if  not request.session.get('is_login', None):
        login_form = UserForm()
        return render(request, os.path.join(PROJECT_ROOT,'MLWebService/templates','login.html'), locals())
    else: return render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates','upload.html'))

def startTrainModel(request,id):
    if request.method=="POST":
        waitTraining =trainingTask.objects.filter(oid=id)
        #训练模型
        task = waitTraining[0]
        task.onTraining = 0
        td = learnThread(task.trainingName,task.trainingDataFile,task.typeOfModel)
        task.save()
        td.start()
        return HttpResponseRedirect(reverse("tasks")) #返回一个reverse
    return HttpResponse("error")

def deleteModel(request,id):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method=="POST":
        deleteTask =trainingTask.objects.filter(oid=id)
        #训练模型
        task = deleteTask[0]
        modelPath = os.path.join(PROJECT_ROOT,'MLWebService\CompleteModels',task.modelName)
        if(os.path.exists(modelPath)):
            os.remove(modelPath)
        dataPath = deleteModel.trainingDataFile
        moreTasks =trainingTask.objects.filter(DataFile=dataPath) #检查是否有共用数据文件的任务
        if len(moreTasks)==1:
            os.remove(dataPath)
        task.delete()
        return HttpResponseRedirect(reverse("tasks")) #返回一个reverse
    return HttpResponse("error")

def showTasks(request):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if  not request.session.get('is_login', None):
        login_form = UserForm()
        return render(request, os.path.join(PROJECT_ROOT,'MLWebService/templates','login.html'), locals())
    onTrainingModel = trainingTask.objects.filter(onTraining=0)
    dir_list = os.listdir(os.path.join(PROJECT_ROOT,'MLWebService/CompleteModels'))
    for mod in onTrainingModel:
        if mod.trainingName+".model" in dir_list: #检查是否有模型文件
            mod.onTraining=1
            mod.save()
        else:continue
    results = trainingTask.objects.filter(username=request.session.get('user_name'))
    return  render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates/tasks.html'),{"data": results.all()})

def showTest(request,id):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    onTestModel = trainingTask.objects.filter(oid=id)[0]
    modelFile = os.path.join(PROJECT_ROOT,'MLWebService/CompleteModels',onTestModel.trainingName+'.model')
    Mod = joblib.load(modelFile)
    t =os.path.getctime(modelFile)
    t =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t))
    f = open(onTestModel.trainingDataFile,"r")
    first_line = f.readline()
    return render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates/test.html'),{"MoDel":onTestModel,\
        "score":Mod.steps[2][1].best_score_,"time":t,"features":first_line})

def startTest(request,id):
    testData = request.POST.get('testData')
    onTestModel = trainingTask.objects.filter(oid=id)[0]
    modelFile = os.path.join(PROJECT_ROOT,'MLWebService/CompleteModels',onTestModel.trainingName+'.model')
    Mod = joblib.load(modelFile)
    testData = testData.split('\n')
    data = []
    for line in testData:
        line = line.split()
        dataLine = [float(dat) for dat in line]
        data.append(dataLine)
    result = Mod.predict(data)
    result = np.c_[data,result]
    print(result)
    return testResult(request,id,result)

def testResult(request,id,result):
    onTestModel = trainingTask.objects.filter(oid=id)[0]
    f = open(onTestModel.trainingDataFile,"r")
    first_line = f.readline()
    features = [first_line.split()]
    result= np.r_[features,result]
    #return HttpResponse("error")
    return render(request,os.path.join(PROJECT_ROOT,'MLWebService/templates/results.html'),{"data":result})