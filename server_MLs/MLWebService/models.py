from django.db import models

# Create your models here.

class trainingTask(models.Model):
    oid = models.AutoField(primary_key=True)
    traingName = models.CharField(max_length=200)
    trainingDataFile = models.CharField(max_length = 200)
    typeOfModel = models.CharField(max_length = 100)
    onTraining = models.BooleanField(default="False")
    uploadTime = models.TimeField(auto_now="True")
    