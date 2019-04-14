from django.db import models

# Create your models here.

class trainingTask(models.Model):
    oid = models.IntegerField(primary_key=True, db_column='FId')
    trainingName = models.CharField(max_length=200)
    trainingDataFile = models.CharField(max_length = 200)
    typeOfModel = models.CharField(max_length = 100)
    onTraining = models.IntegerField(default=-1)
    uploadTime = models.DateTimeField(auto_now="True")