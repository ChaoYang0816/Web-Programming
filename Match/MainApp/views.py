from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import User, Hobby, Like
from operator import attrgetter
import datetime as D
import time
from django.utils import timezone
from django.core import serializers

# Render the log in page
def index(req):
    return render(req, 'MainApp/index.html', {})

# Access the profile page
def login(req):
    if req.method == 'POST':
        email = req.POST['email']
        pwd = req.POST['pwd']

        # Find user by email and password
        user = User.objects.filter(email=email)

        # Find all users except logged in user
        users = User.objects.exclude(email=email)

        if len(user) == 0:
            errorMsg = "User does not exist"

            return render(req, 'MainApp/index.html', { 'errorMsg': errorMsg })
        elif len(user) != 0 and user[0].password != pwd:
            errorMsg = "Invalid password. Please enter the correct password!"

            return render(req, 'MainApp/index.html', { 'errorMsg': errorMsg })
        else:
            list = sort(user, users)

            likes = []
            for like in user[0].likes.all():
                likes.append(like.email)

            # Setting the sessions
            req.session['email'] = email
            req.session['pwd'] = pwd

            response = render(req, 'MainApp/profile.html', { 'user': user[0], 'users': list, 'likes': likes })

            # Setting the cookies
            now = D.datetime.utcnow()
            max_age = 365 * 24 * 60 * 60  #one year
            delta = now + D.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = D.datetime.strftime(delta, format)
            response.set_cookie('last_login', now, expires=expires)
            return response
    else:
        raise Http404('Something went wrong !')


# Logging out from the profile page
def logout(req):
    # Check if sessions still available
    if 'email' in req.session:
        req.session.flush()
        print("Your session is deleted")
    return render(req, 'MainApp/index.html', {})


def register(req):
    if req.method == 'GET':
        hobbyList = Hobby.objects.all().values('hobbyName', 'hobbyInfo')

        return render(req, 'MainApp/register.html', { 'hobbyList': hobbyList })
    else:
        raise Http404("Something went wrong !", {})

def newUser(req):
    if req.method == 'POST':
        firstName = req.POST['firstName']
        lastName = req.POST['lastName']
        age = req.POST['age']
        dob = req.POST['dob']
        gender = req.POST.get('gender')
        email = req.POST['email']
        password = req.POST['pwd']
        profilePic = req.FILES['profilePic']
        hobbies = req.POST.getlist('hobby')

        users = User.objects.filter(email=email)

        if len(users) == 0:
            #Creating a new user to be saved into the DB
            user = User(firstName=firstName, lastName=lastName, age=age, dob=dob, gender=gender, email=email, password=password, profilePic=profilePic)
            user.save()

            #Adding hobbies to user
            for hobbyName in hobbies:
                hobby = Hobby.objects.get(pk=hobbyName)
                user.hobbies.add(hobby)

            return render(req, 'MainApp/index.html', {})
        else:
            errorMsg = "This e-mail is taken. Please use a different email."

            return render(req, 'MainApp/register.html', { 'errorMsg': errorMsg })
    else:
        raise Http404('Something went wrong !')

@csrf_exempt
def sortUserList(req):
    sortedList = []
    if req.method == 'POST':
        Age_1 = req.POST['minAge']
        Age_2 = req.POST['maxAge']
        gender = req.POST['gender']
        email = req.POST['email']
        #To check if min and max ages fields used for sort
        if Age_1 == '':
            minAge = 0
        else:
            minAge = int(Age_1)
        if Age_2 == '':
            maxAge = 0
        else:
            maxAge = int(Age_2)
        user = User.objects.filter(email = email)
        #Filters user list by sort gender selected
        users = User.objects.filter(gender=gender).exclude(email=email)
        listSort = sort(user, users)
        #If max age input, normal age check
        if maxAge != 0:
            #Checks ages of each user in list against sort ages selected
            for u in listSort:
                if u.age < minAge or u.age > maxAge:
                    continue
                else:
                    sortedList.append(u)
            userList = list(sortedList)
        #If max age not input, only check ages for min age
        else:
            #Checks ages of each user in list against sort ages selected
            for u in listSort:
                if u.age < minAge:
                    continue
                else:
                    sortedList.append(u)
            userList = list(sortedList)
        #print(userList)
        data = serializers.serialize('json', userList)
        return JsonResponse(data, safe=False)
    else:
        raise Http404("Something went wrong!")

# Method to sort the users from most to least matching hobbies
def sort(user, users):
    hobbies = user[0].hobbies.all()
    i = 0
    #Compares other users' hobbies to logged in user and adds new field 'hobbyCount' with value of similar hobbies
    for u in users:
        k = 0
        h = u.hobbies.all()
        for hobby in hobbies:
            if hobby in h:
                k += 1
        users[i].hobbyCount = k
        i += 1

    #Sorts user list by newly added field 'hobbyCount'
    list = sorted(users, key=attrgetter('hobbyCount'), reverse=True)

    return list

#Method for logged in user to Like any other users
def like(request):
    if request.method == 'PUT':
        put = QueryDict(request.body)
        fromU = put.get('fromUser')
        to = put.get('toUser')

        t = D.datetime.now(tz=timezone.utc)

        fromUser = User.objects.get(email = fromU)
        toUser = User.objects.get(email = to)

        likedUser = Like(fName = toUser.firstName, lName = toUser.lastName, email = toUser.email, dtime = t)
        likedUser.save()

        #Adds liked user's object to logged in user's 'likes' field
        fromUser.likes.add(likedUser)

        users = list(User.objects.exclude(email = fromUser.email).values())

        return JsonResponse(users, safe=False)
    else:
        raise Http404("Something went wrong!")

#Method for logged in user to Dislike any previously liked users
def dislike(request):
    if request.method == 'PUT':
        put = QueryDict(request.body)
        fromU = put.get('fromUser')
        to = put.get('toUser')

        fromUser = User.objects.get(email = fromU)

        #Deletes disliked user's object from logged in user's 'likes' field
        fromUser.likes.get(email = to).delete()

        users = list(User.objects.exclude(email = fromUser.email).values())

        return JsonResponse(users, safe=False)
    else:
        raise Http404("Something went wrong!")

#@csrf_exempt
#def checkUser(request):
#    if request.method == 'GET':
#        input = request.GET['input']
#        ans = ""
#
#        check = User.objects.filter(email = input)
#
#        if(len(check) == 0):
#            ans = "Username is valid."
#            print(ans)
#            return JsonResponse(ans, safe=False)
#        else:
#            ans = "Username is already taken."
#            print(ans)
#            return HttpResponse(ans)
#    else:
#        raise Http404("Something went wrong!")
