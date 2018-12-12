from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import User, Hobby, Like
from operator import attrgetter
import datetime as D
import time
from django.utils import timezone

# Render the log in page
def index(req):
    return render(req, 'MainApp/index.html', {})

# Access the profile page
def login(req):
    if req.method == 'POST':
        email = req.POST['email']
        pwd = req.POST['pwd']

        # Find user by email and password
        user = User.objects.filter(email=email, password=pwd)

        # Find all users except logged in user
        users = User.objects.exclude(email=email)

        if len(user) == 0:
            errorMsg = "User does not exist"

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

        #Variable to validate email and password
        taken = False

        users = User.objects.filter(email=email, password=password)

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
            #Checking if user exists
            for i in range(len(users)):
                if (users[i].email == email) or (users[i].password == password):
                    taken = True

                    break
                else:
                    taken = False

            #Generating error message
            if taken:
                errorMsg = "E-mail and password are already taken"

                return render(req, 'MainApp/index.html', { 'errorMsg': errorMsg })
            else:
                #Creating a new user to be saved into the DB
                user = User(firstName=firstName, lastName=lastName, age=age, dob=dob, gender=gender, email=email, password=password, profilePic=profilePic)
                user.save()

                #Adding hobbies to user
                for hobbyName in hobbies:
                    hobby = Hobby.objects.get(pk=hobbyName)
                    user.hobbies.add(hobby)

                return render(req, 'MainApp/index.html', {})
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
        minAge = int(Age_1)
        maxAge = int(Age_2)

        user = User.objects.filter(email = email)
        users = User.objects.filter(gender=gender).exclude(email=email)

        listSort = sort(user, users)

        for u in listSort:
            if u.age >= minAge and u.age <= maxAge:
                sortedList.append(u)

        userList = list(sortedList)

        return JsonResponse(userList, safe=False)
    else:
        raise Http404("Something went wrong!")

# Method to sort the users from most to least matching hobbies
def sort(user, users):
    hobbies = user[0].hobbies.all()
    i = 0
    for u in users:
        k = 0
        h = u.hobbies.all()
        for hobby in hobbies:
            if hobby in h:
                k += 1
        users[i].hobbyCount = k
        #print(users[i].hobbyCount)
        i += 1

    list = sorted(users, key=attrgetter('hobbyCount'), reverse=True)

    return list

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

        fromUser.likes.add(likedUser)

        users = list(User.objects.exclude(email = fromUser.email).values())

        return JsonResponse(users, safe=False)
    else:
        raise Http404("Something went wrong!")

def dislike(request):
    if request.method == 'PUT':
        put = QueryDict(request.body)
        fromU = put.get('fromUser')
        to = put.get('toUser')

        fromUser = User.objects.get(email = fromU)

        fromUser.likes.get(email = to).delete()

        users = list(User.objects.exclude(email = fromUser.email).values())

        return JsonResponse(users, safe=False)
    else:
        raise Http404("Something went wrong!")

@csrf_exempt
def checkUser(request):
    if request.method == 'GET':
        input = request.GET['input']
        ans = ""

        check = User.objects.filter(email = input)

        if(len(check) == 0):
            ans = "Username is valid."
            print(ans)
            return JsonResponse(ans, safe=False)
        else:
            ans = "Username is already taken."
            print(ans)
            return HttpResponse(ans)
    else:
        raise Http404("Something went wrong!")
