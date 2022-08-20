from tkinter import CASCADE
from unicodedata import decimal
from django.db import models

class Hotel(models.Model):
    name        = models.TextField()
    IVA         = models.TextField()
    street      = models.TextField()
    stars       = models.DecimalField(max_digits=1, decimal_places=0)
    rooms_count = models.DecimalField(max_digits=3, decimal_places=0)
    free_time   = models.TextField()
    CAP         = models.DecimalField(max_digits=5, decimal_places=0)
    city        = models.TextField()
    description = models.TextField()

class Rooms(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    name = models.TextField()
    people = models.TextField()
    size = models.DecimalField(max_digits=2, decimal_places=0)
    description = models.TextField()
    photo = models.FileField(upload_to='static/user_photo')

class Cost(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    begin_date = models.DateField()
    end_date = models.DateField() 
