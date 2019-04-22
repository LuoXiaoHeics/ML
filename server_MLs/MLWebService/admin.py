from django.contrib import admin

# Register your models here.
from .models import trainingTask
from .models import MLUser
admin.site.register(trainingTask)
admin.site.register(MLUser)