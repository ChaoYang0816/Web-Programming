from django.db import models

# User and Hobby models have a many to many relationship

# Hobby model for DB
class Hobby(models.Model):
    hobbyName = models.CharField(max_length=10, primary_key=True)
    hobbyInfo = models.TextField(max_length=3000)

# Like model for DB
class Like(models.Model):
    fName = models.CharField(max_length=20)
    lName = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

# User model for DB
class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    profilePic = models.ImageField(upload_to="profile_images", blank=True)
    hobbies = models.ManyToManyField(Hobby)
    likes = models.ManyToManyField(Like)
