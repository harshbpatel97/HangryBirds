from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import auth
from .models import UserTable
from django.views.decorators.csrf import csrf_exempt


def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render())


def signup(request):
    if request.method == 'POST':
        newUser = UserTable()
        newUser.username = request.POST['username']
        if UserTable.objects.filter(username=newUser.username).exists():
            print("Username already exists")
            return HttpResponse("Username already exists")
        
        else:
            newUser.email = request.POST['email']
            newUser.password = request.POST['password']
            newUser.save()
            template = loader.get_template("home.html")
            return HttpResponse(template.render())
           
        
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def login(request):
     template = loader.get_template("login.html")
     return HttpResponse(template.render())

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if UserTable.objects.filter(username=username, password=password).exists():
            template = loader.get_template("index.html")
            return HttpResponse(template.render())
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        # show an error page
        form = UserCreationForm()
        print("User doesn't exists")
        return render(request=request,
                      template_name="login.html",
                      context={"form": form})  # add error page link


def logout_view(request):
    logout(request)
    # redirect to a success page
    return HttpResponseRedirect()  # add page link
