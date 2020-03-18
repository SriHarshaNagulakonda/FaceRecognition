from django.db import models

class Criminal(models.Model):
    name=models.CharField(max_length=100)
    crime=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    embedding=models.CharField(max_length=20000)
    photo=models.ImageField(upload_to='photos/')
