from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import auth, sessions
from .models import UserTable
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from passlib.hash import pbkdf2_sha256


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
        username = request.session['username']
        return render(request, 'index.html', {"username" : username})
    else:
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
                return render(request, "index.html", {"username" : username})
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
