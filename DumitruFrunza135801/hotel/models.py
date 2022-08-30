from tkinter import CASCADE
from unicodedata import decimal
from django.db import models
from django.contrib.auth.models import User

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

class Activity(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    one_activity = models.TextField()

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits = 10, decimal_places=2)