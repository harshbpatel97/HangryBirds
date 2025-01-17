"""HangryBirds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from home import views

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^home/', include('home.urls')),
                  url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
                  url(r'^signup/', views.signup, name="signup"),
                  url(r'^login/', views.login, name="login"),
                  url(r'^login_view/', views.login_view, name="login_view"),
                  url(r'^index', TemplateView.as_view(template_name='index.html'), name='index'),
                  url(r'^logout/', views.logout, name = 'logout'),
                  url(r'^showReview/(?P<parameter>[\w-]+)', views.showReview, name="showReview"),
                  url(r'^writeReview/(?P<parameter>[\w-]+)', views.writeReview, name="writeReview"),
                  url(r'^showMyReviews/', views.showMyReviews, name="showMyReviews"),
                  url(r'^deleteReview/(?P<parameter>[\w-]+)', views.deleteReview, name="deleteReview"),
                  url(r'^updateReview/', views.updateReview, name = 'updateReview'),
                  url(r'^loadFoodSearch/', views.loadFoodSearch, name = 'loadFoodSearch'),
                  url(r'^get_queryset_food/', views.get_queryset_food, name = 'get_queryset_food'),
                  url(r'^loadRestSearch/', views.loadRestSearch, name = 'loadRestSearch'),
                  url(r'^get_queryset_rest/', views.get_queryset_rest, name = 'get_queryset_rest'),
                  url(r'^redirectFoodSearch/(?P<parameter>[\w-]+)', views.redirectFoodSearch, name="redirectFoodSearch"),
                  url(r'^deleteReviewByAdmin/(?P<parameter>[\w-]+)', views.deleteReviewByAdmin, name="deleteReviewByAdmin"),
                  url(r'^pendingItemRequest/(?P<parameter>[\w-]+)', views.pendingItemRequest, name="pendingItemRequest"),
                  url(r'^redirectPending/', views.redirectPending, name="redirectPending"),
                  url(r'^approveItemRequest/(?P<parameter>[\w-]+)', views.approveItemRequest, name="approveItemRequest"),
                  url(r'^declineItemRequest/(?P<parameter>[\w-]+)', views.declineItemRequest, name="declineItemRequest"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
