from django.db import models
from login_app.models import User

class ActivityManager(models.Manager):
    def validator(self, postData):
        errors ={}
        if not postData['title']:
            errors['title'] = 'Title is required!'
        if len(postData['title']) > 100:
            errors['title'] = 'Exceeded Maximum Length!'

        if not postData['location']:
            errors['location'] = 'Location is required!'

        if not postData['description']:
            errors['description'] = 'Description is required!'
        if len(postData['description']) < 10:
            errors['description'] = 'Description should be at least ten characters!'

        if not postData['price']:
            errors['price'] = 'Price is required! It can be zero though.'

        if not postData['city']:
            errors['city'] = 'City is required!'

        return errors

class City(models.Model):
    name = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #activities = list of activities in this certain city.

class Activity(models.Model):
    title = models.CharField(max_length = 100)
    location = models.CharField(max_length = 255)
    start_date = models.DateTimeField(null = True)
    end_date = models.DateTimeField(null = True)
    desc = models.TextField()
    price = models.IntegerField()
    added_by = models.ForeignKey(User, related_name='activities_added', on_delete = models.CASCADE)
    city = models.ForeignKey(City, related_name='activities', on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name='liked_activities')
    users_who_dislike = models.ManyToManyField(User, related_name='disliked_activities')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ActivityManager()

