from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import auth, sessions
from .models import UserTable, RestaurantTable, MenuTable, ReviewTable
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
import datetime

def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render())


def signup(request):
    if request.method == 'POST':
        newUser = UserTable()
        newUser.username = request.POST['username']
        if UserTable.objects.filter(username=newUser.username).exists():
            print("Username already exists")
            messages.info(request, 'Username already exists')
            return render(request, "signup.html")
            #return HttpResponse("Username already exists")
        
        else:
            newUser.email = request.POST['email']
            password = request.POST['password']
            newUser.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            newUser.save()
            template = loader.get_template("home.html")
            return HttpResponse(template.render())
           
        
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def login(request):
    if request.session.has_key('username'):
        print("in if condition")
        username = request.session['username']
       
        return render(request, 'index.html', {'username': username})
    else:
        print("in else condition")
        return render(request, 'login.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = UserTable.objects.filter(username=username)
        user = users.first()
        if user != None:
            if pbkdf2_sha256.verify(password,user.password):
                request.session['username'] = username
                restData = RestaurantTable.objects.all()
                restVar = {
                    "rest_ID": restData,
                    "username": username
                }
                return render(request, "index.html", restVar)
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            messages.info(request, 'Invalid login details!')
            return render(request, "login.html")
            #return HttpResponse("Invalid login details given")
    else:
        # show an error page
        form = UserCreationForm()
        print("User doesn't exists")
        messages.info(request, "User doesn't exists!")
        return render(request=request,
                      template_name="login.html",
                      context={"form": form})  # add error page link

def logout(request):
   try:
      del request.session['username']
      messages.info(request, 'You have been successfully logged out!')
   except:
      pass
   return render(request, "home.html")

def showReview(request, parameter):
    if request.session.has_key('username'):
        username = request.session['username']
        rest_ID = parameter
        restData = RestaurantTable.objects.get(rest_ID=rest_ID)
        menuData = MenuTable.objects.filter(restObj=rest_ID)
        reviewData = ReviewTable.objects.filter(restObj=rest_ID)
        restVar = {
            "rest_ID": restData,
            "username": username,
            "menu_ID": menuData,
            "review_ID": reviewData,
        }
        return render(request, 'showReview.html', restVar)

def writeReview(request, parameter):
    if request.method == 'POST':
        newReview = ReviewTable()
        username = request.session['username']
        newReview.review = request.POST['reviewText']
        newReview.rating = request.POST['rating']
        newReview.timestamp = datetime.datetime.now()
        newReview.userObj = UserTable.objects.get(username=username)
        newReview.menuObj = MenuTable.objects.get(item_ID=parameter)
        newReview.restObj = MenuTable.objects.get(item_ID=parameter).restObj
        newReview.save()
        template = loader.get_template("showReview.html")
        return HttpResponse(template.render())
    
    else:
        template = loader.get_template("home.html")
        return HttpResponse(template.render())
    
        