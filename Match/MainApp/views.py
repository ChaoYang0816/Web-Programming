from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .models import Hobby

# Render the log in page
def index(req):
    return render(req, 'MainApp/index.html', {})

@csrf_exempt
def log(req):
    if req.method == 'GET':
        email = req.GET['email']
        pwd = req.GET['pwd']

        user = User.objects.filter(email=email, password=pwd)
        # .values('firstName', 'lastName', 'age', 'dob', 'gender', 'email', 'profilePic', 'hobbies')
        print(user)

        return render(req, 'MainApp/profile.html', {"user": user[0]})

@csrf_exempt
def register(req):
    if req.method == 'GET':
        hobbyList = Hobby.objects.all().values('hobbyName', 'hobbyInfo')

        return render(req, 'MainApp/register.html', { 'hobbyList': hobbyList })
    else:
        raise Http404("Something went wrong !", {})

@csrf_exempt
def newUser(req):
    if req.method == 'POST':
        firstName = req.POST['firstName']
        lastName = req.POST['lastName']
        age = req.POST['age']
        dob = req.POST['dob']
        gender = req.POST.get('gender')
        email = req.POST['email']
        password = req.POST['pwd']
        profilePic = req.POST['profilePic']
        hobbies = req.POST.getlist('hobby')

        #creating a new user to be saved into the DB
        user = User(firstName=firstName, lastName=lastName, age=age, dob=dob, gender=gender, email=email, password=password, profilePic=profilePic)
        user.save()

        #adding hobbies to user
        for hobbyName in hobbies:
            hobby = Hobby.objects.get(pk=hobbyName)
            user.hobbies.add(hobby)


        return render(req, 'MainApp/index.html', {})
    else:
        raise Http404('Something went wrong !')
