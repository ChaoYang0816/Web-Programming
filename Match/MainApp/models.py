from django.db import models

# Create your models here.
class Hobby(models.Model):
    hobbyName = models.CharField(max_length=10, primary_key=True)
    hobbyInfo = models.TextField(max_length=3000)

class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    profilePic = models.ImageField()
    hobbies = models.ManyToManyField(Hobby)
