from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import auth
from .models import UserTable


def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render())


def signup(request):
    if request.method == 'POST':
        #form = UserCreationForm(data=request.POST)

        # if form.is_valid():
        #print("Form is submitted")
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["psw"]
        user = UserTable(username=username, email=email, password=password)
        user.save()
        template = loader.get_template("login.html")
        return HttpResponse(template.render())

        # else:
        #     print("Form not submitted")
        #     for msg in form.error_messages:
        #         print(form.error_messages[msg])
        #     return render(request=request,
        #                   template_name="signup.html",
        #                   context={"form": form})
    else:
        form = UserCreationForm()
        return render(request=request,
                      template_name="signup.html",
                      context={"form": form})


def login(request):
    template = loader.get_template("login.html")
    return HttpResponse(template.render())


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get['uname']
        password = request.POST.get['psw']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # correct password, and the user is marked "active"
                login(request, user)
                # redirect to the success page
                template = loader.get_template("index.html")
                return HttpResponse(template.render())
            else:
                return HttpResponse("Your account was inactive")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        # show an error page
        return HttpResponseRedirect()  # add error page link


def logout_view(request):
    logout(request)
    # redirect to a success page
    return HttpResponseRedirect()  # add page link
