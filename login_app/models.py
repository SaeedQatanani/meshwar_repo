from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def user_validator(self, postData, index):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if index == 1:
            if not postData['first_name']:
                errors["first_name"] = "Please insert your first name."
            else:
                if len(postData['first_name']) < 2:
                    errors["first_name"] = "First name should be at least two characters!"
                if  str(postData['first_name']).isalpha() == False:
                    errors['first_name'] = "First name should contain characters only."

            if not postData['last_name']:
                errors["last_name"] = "Please insert your last name."
            else:
                if len(postData['last_name']) < 2:
                    errors["last_name"] = "Last name should be at least two characters!"
                if  str(postData['last_name']).isalpha() == False:
                    errors['last_name'] = "Last name should contain characters only."

            if not postData['email']:
                errors["email"] = "Please insert an E-mail."
            else:
                if not EMAIL_REGEX.match(postData['email']):
                    errors['email_validation'] = "Invalid email address!"
                for user in User.objects.all():
                    if user.email == postData['email']:
                        errors["email_uniqueness"] = "This E-mail is already used! Try another one."

            if not postData['password'] or not postData['confirm_pw']:
                errors["password"] = "Please insert a password and make sure to confirm it."
            else:
                if len(postData['password']) < 8:
                    errors["password"] = "Password should be at least eight characters!"
                else:
                    if postData['password'] != postData['confirm_pw']:
                        errors["password_confirm"] = "Passwords do not match! Please try again."

            if not postData['birthday']:
                errors["missing_field_birthday"] = "Please insert your date of birth."
            else:
                if datetime.strptime(postData['birthday'], '%Y-%m-%d') >= datetime.today():
                    errors["birthday"] = "You should be born in the past!"
                elif (datetime.today() - datetime.strptime(postData['birthday'], '%Y-%m-%d')).days/365 < 13:
                    errors["birthday_age"] = "You should be older than 13 years old! Come back when you are old enough."

        if index == 2:
            if not postData['login_email']:
                errors["login_email"] = "Please insert an E-mail."
            else:
                if not EMAIL_REGEX.match(postData['login_email']):
                    errors['login_email_validation'] = "Invalid email address!"
                for user in User.objects.all():
                    flag = False
                    if user.email == postData['login_email']:
                        flag = True
                        break
                if flag == False:
                    errors["login_email_exsistance"] = "This E-mail has not registered yet! Complete the registration form."

            if not postData['login_password']:
                errors["missing_field_login_password"] = "Please insert your password."
            else:
                if len(postData['login_password']) < 8:
                    errors["login_password_length"] = "Your Password has to be at least eight characters! Try again."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    birthday = models.DateField()
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #activities_added = a list of added activities
    #liked_activities = a list of liked activities
    #disliked_activities = a list of dis-liked activities