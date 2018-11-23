from django.db import models

# Create your models here.
class Hobby(models.Model):
    hobbyName = models.CharField(max_length=10, primary_key=True)
    hobbyInfo = models.TextField(max_length=3000)

class User(models.Model):
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=10)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=8)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    profilePic = models.ImageField(upload_to='profile_images')
    hobbies = models.ManyToManyField(Hobby)
