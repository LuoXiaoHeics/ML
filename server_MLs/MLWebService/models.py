from django.db import models

# Create your models here.

class trainingTask(models.Model):
    traingName = models.CharField(max_length=200,primary_key=True)
    trainingDataFile = models.CharField(max_length = 200)
    typeOfModel = models.CharField(max_length = 100)
    onTraining = models.IntField(default=-1)
    uploadTime = models.TimeField(auto_now="True")

class trainingModels(models.Model):
    trainingNmae = models.CharField(primary_key=True)
    modelFile = models.CharField(max_length = 200)
    rate = models.FloatField()
    typeOfModel = models.CharField(max_length = 100)