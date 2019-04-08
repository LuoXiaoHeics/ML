# Generated by Django 2.1.1 on 2019-04-07 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='trainingTask',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('traingName', models.CharField(max_length=200)),
                ('trainingDataFile', models.CharField(max_length=200)),
                ('typeOfModel', models.CharField(max_length=100)),
                ('onTraining', models.BooleanField(default='False')),
            ],
        ),
    ]
