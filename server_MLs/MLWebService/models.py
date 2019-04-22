from django.db import models

# Create your models here.

class trainingTask(models.Model):
    oid = models.IntegerField(primary_key=True, db_column='FId')
    trainingName = models.CharField(max_length=200)
    trainingDataFile = models.CharField(max_length = 200)
    typeOfModel = models.CharField(max_length = 100)
    onTraining = models.IntegerField(default=-1)
    uploadTime = models.DateTimeField(auto_now="True")
    username = models.CharField(max_length=128,default = "")

class MLUser(models.Model):
    '''用户表'''
    username = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.username
 
    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'