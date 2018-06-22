from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def regValidator(self, postData):
        errors = {}
        if len(postData['first_name'])<2 or not postData['first_name'].isalpha():
            errors['first_name'] = "First Name is not long enough"
        if len(postData['last_name'])<2 or not postData['last_name'].isalpha():
            errors['last_name'] = "Last Name is not long enough"
        if User.objects.filter(email = postData['email']):
            errors['email_exists'] = "Email is already Registered"
        if EMAIL_REGEX.match(postData['email']) == None:
            errors['email_format'] = "Email must be a valid format"
        if len(postData['password'])<8:
            errors['password'] = "Invalid Password! Must have no fewer than 8 characters"
        if postData['password'] != postData['verifypass']:
            errors['verifypass'] = "Password confirmation must match password."
        # if postData['birthday'] > datetime.date.today():
        #     errors['birthday'] = "Date Format is incorrect, enter a valid Birthday."
        return errors

    def loginValidator(self, postData):
        user = User.objects.filter(email = postData['email_login']).first()
        errors = {}
        if not user:
            errors['email'] = "Please Enter Valid Email"
        elif not bcrypt.checkpw(postData['password_login'].encode('utf8'), user.password.encode('utf8')):
            errors['email'] = "Invalid Password"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = UserManager()

    def __repr__(self):
        return f'User(first_name = {self.first_name},last_name = {self.last_name}, email = {self.email})'

    
#adding to models.Manager function by setting objects equal