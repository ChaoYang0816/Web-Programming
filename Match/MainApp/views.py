from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .models import Hobby

# Render the log in page
def index(req):
    return render(req, 'MainApp/index.html', {})

@csrf_exempt
def login(req):
    if req.method == 'POST':
        email = req.POST['email']
        pwd = req.POST['pwd']

        user = User.objects.filter(email=email, password=pwd)

        if len(user) == 0:
            errorMsg = "User does not exist"

            return render(req, 'MainApp/index.html', { 'errorMsg': errorMsg })
        else:
            return render(req, 'MainApp/profile.html', { 'user': user[0] })
    else:
        raise Http404('Something went wrong !')

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

        #variable to validate email and password
        taken = False

        users = User.objects.filter(email=email, password=password)

        if len(users) == 0:
            #creating a new user to be saved into the DB
            user = User(firstName=firstName, lastName=lastName, age=age, dob=dob, gender=gender, email=email, password=password, profilePic=profilePic)
            user.save()

            return render(req, 'MainApp/index.html', {})
        else:
            #checking if user exists
            for i in range(len(users)):
                if (users[i].email == email) or (users[i].password == password):
                    taken = True

                    break
                else:
                    taken = False

            #generating error message
            if taken:
                errorMsg = "E-mail and password are already taken"

                return render(req, 'MainApp/index.html', { 'errorMsg': errorMsg })
            else:
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
