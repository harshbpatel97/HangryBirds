from django.db import models

# Create your models here.

class UserTable(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.username


class RestaurantTable(models.Model):
    rest_ID = models.IntegerField(primary_key=True)
    rest_name = models.CharField(max_length=100)
    rest_loc = models.CharField(max_length=250)
    rest_contact = models.CharField(max_length=15)
    
    def __str__(self):
        return self.rest_ID


class MenuTable(models.Model):
    item_ID = models.IntegerField(primary_key=True)
    restObj = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.item_ID

class ReviewTable(models.Model):
    review_ID = models.IntegerField(primary_key=True)
    userObj = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    menuObj = models.ForeignKey(MenuTable, on_delete=models.CASCADE)
    restObj = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True, editable=True)
    rating = models.IntegerField()
    
    def __str__(self):
        return self.review_ID