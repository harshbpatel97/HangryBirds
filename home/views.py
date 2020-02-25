from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import auth


def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render())


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            template = loader.get_template("login.html")
            return HttpResponse(template.render())

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request=request,
                          template_name="signup.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="signup.html",
                  context={"form": form})


def login(request):
    template = loader.get_template("login.html")
    return HttpResponse(template.render())


def login_view(request):
    username = request.POST['uname']
    password = request.POST['psw']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        #correct password, and the user is marked "active"
        auth.login(request, user)
        #redirect to the success page
        template = loader.get_template("index.html")
        return HttpResponse(template.render())
    else:
        #show an error page
        return HttpResponseRedirect() #add error page link


def logout_view(request):
    auth.logout(request)
    #redirect to a success page
    return HttpResponseRedirect() #add page link