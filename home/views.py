from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import auth, sessions
from .models import UserTable, RestaurantTable, MenuTable, ReviewTable, PendingMenuTable
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
import datetime
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from django.db.models import Q

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
        if username == "Admin":
            request.session['username'] = username
            reviewData = ReviewTable.objects.all()
            reviewVar = {
                "reviewData": reviewData,
                "username": username
            }
            return render(request, "admin.html", reviewVar)
        
        restData = RestaurantTable.objects.all()
        restVar = {
            "rest_ID": restData,
            "username": username
        }
        return render(request, 'index.html', restVar)
    else:
        return render(request, 'login.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = UserTable.objects.filter(username=username)
        user = users.first()
        if username == "Admin":
            if pbkdf2_sha256.verify(password,user.password):
                request.session['username'] = username
                reviewData = ReviewTable.objects.all()
                reviewVar = {
                    "reviewData": reviewData,
                    "username": username
                }
                return render(request, "admin.html", reviewVar)
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username, password))
                messages.info(request, 'Invalid login details!')
                return render(request, "login.html")
        
        elif user != None:
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
        messages.info(request, 'Thanks for submitting the review')
        return login(request)
        
    else:
        template = loader.get_template("home.html")
        return HttpResponse(template.render())
    
def showMyReviews(request):
    if request.session.has_key('username'):
        username = request.session['username']
        userData = UserTable.objects.filter(username=username)
        reviewData = ReviewTable.objects.filter(userObj__in=userData)
        reviewVar = {
            "username": username,
            "userID": userData,
            "review_ID": reviewData,
        }
        return render(request, 'myReviews.html', reviewVar)
        
def deleteReview(request, parameter):
    if request.session.has_key('username'):
        ReviewTable.objects.filter(id=parameter).delete()
        messages.info(request, 'You have successfully deleted your review')
        return showMyReviews(request)

def updateReview(request):
    reviewObj = ReviewTable.objects.get(id=request.POST['review_ID'])
    reviewObj.review = request.POST['review_text']
    reviewObj.rating = request.POST['rating_text']
    reviewObj.timestamp = datetime.datetime.now()
    reviewObj.save()
    messages.info(request, 'You have successfully updated your review')
    print("Updated")
    return showMyReviews(request)
    
def loadFoodSearch(request):
    username = request.session['username']
    userData = {
        "username": username
    }
    return render(request, 'search_food.html', userData)


@csrf_exempt
def get_queryset_food(request):
    if request.method == 'POST':
        query = request.POST['inputSearch']
        object_list = MenuTable.objects.filter(Q(item_name__icontains=query))
        username = request.session['username']
        foodVar = {
            "object_list" : object_list,
            "query": query,
            "username": username
        }
        messageStr = str(len(object_list)) + " result/s found!!!"
        messages.info(request, messageStr)
        return render(request, 'search_food.html', foodVar)


def redirectFoodSearch(request, parameter):
    if request.session.has_key('username'):
        username = request.session['username']
        item_ID = parameter
        print(item_ID)
        rest_ID = MenuTable.objects.filter(item_ID=item_ID).first().restObj.rest_ID
        restData = RestaurantTable.objects.get(rest_ID=rest_ID)
        menuData = MenuTable.objects.filter(restObj=rest_ID)
        reviewData = ReviewTable.objects.filter(restObj=rest_ID)
        restVar = {
            "rest_ID": restData,
            "username": username,
            "menu_ID": menuData,
            "review_ID": reviewData,
            "item_ID": item_ID,
        }
        return render(request, 'showReview.html', restVar)


def loadRestSearch(request):
    username = request.session['username']
    userData = {
        "username": username
    }
    return render(request, 'search_rest.html', userData)
    
@csrf_exempt
def get_queryset_rest(request):
    if request.method == 'POST':
        query = request.POST['inputSearch']
        username = request.session['username']
        object_list = RestaurantTable.objects.filter(Q(rest_name__icontains=query))
        foodVar = {
            "object_list" : object_list,
            "query": query,
            "username": username
        }
        messageStr = str(len(object_list)) + " result/s found!!!"
        messages.info(request, messageStr)
        return render(request, 'search_rest.html', foodVar)
        
def deleteReviewByAdmin(request, parameter):
    ReviewTable.objects.filter(id=parameter).delete()
    messages.info(request, 'You have successfully deleted the review')
    return login(request)
    
def pendingItemRequest(request, parameter):
    if request.method == 'POST':
        newItem = PendingMenuTable()
        username = request.session['username']
        newItem.item_name = request.POST['itemName']
        newItem.restObj = RestaurantTable.objects.get(rest_ID=parameter)
        newItem.userObj = UserTable.objects.get(username=username)
        newItem.save()
        rest_ID = parameter
        messages.info(request, 'Your request is submitted and subject to admin approval!!!')
        return showReview(request, rest_ID)
        
def redirectPending(request):
    if request.session.has_key('username'):
        username = request.session['username']
        pendingItemData = PendingMenuTable.objects.all()
        data = {
            "username": username,
            "pendingItemData": pendingItemData,
        }
        return render(request, 'pendingItem.html', data)
    else:
        return render(request, 'login.html')
        
def approveItemRequest(request, parameter):
    newMenu = MenuTable()
    newMenu.restObj = PendingMenuTable.objects.get(id=parameter).restObj
    newMenu.item_name=PendingMenuTable.objects.get(id=parameter).item_name
    temp =  MenuTable.objects.latest("item_ID").item_ID + 1
    newMenu.item_ID = temp
    newMenu.save()
    messages.info(request, "You have successfully approved the request!!!")
    PendingMenuTable.objects.get(id=parameter).delete()
    return redirectPending(request)
    
def declineItemRequest(request, parameter):
    PendingMenuTable.objects.get(id=parameter).delete()
    messages.info(request, "You have successfully declined the request!!!")
    return redirectPending(request)