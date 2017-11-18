from __future__ import unicode_literals

from django.db import models
import re, bcrypt, time, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
BDAY_REGEX = re.compile(r'^[0-9]{4}[-][0-9]{2}[-][0-9]{2}$')

def num_check(name):
    #checks if the entered password meets our requirements
    has_num = False

    for char in name:
        if char.isdigit():
            has_num = True

    return has_num

def has_upper_num(password):
    #checks if the entered password meets our requirements
    has_upper = False
    has_num = False
    check = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.isdigit():
            has_num = True

    if has_num and has_upper:
        check = True

    return check

# Create your models here.

class UserManager(models.Manager):
    def registration_validation(self, postData):
        errors = {}
        for thing in postData:
            if len(postData[thing]) < 1:
                errors['submit'] = "All fields required"
                return errors
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"

        if len(postData['f_name']) < 2:
            errors['f_name'] = "Name should be more than 2 characters"

        if len(postData['l_name']) < 2:
            errors['l_name'] = "Name should be more than 2 characters"

        if num_check(postData['f_name']):
           errors['f_name'] = "Names must only contain letters"

        if num_check(postData['l_name']):
            errors['l_name'] = "Names must only contain letters"

        if not BDAY_REGEX.match(postData['bday']):
            errors["bday"] = "Birthdate must be in format yyyy-mm-dd"

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"

        if len(postData['pwd']) < 8:
            errors["pwd"] = "Password must be at least 8 characters"
        
        if not has_upper_num(postData['pwd']):
            errors["pwd"] = "Password must contain at least one uppercase letter and one number"

        if postData['pwd_c'] != postData['pwd']:
            errors["pwd_c"] = "Passwords must match"

        records = User.objects.filter(email=postData['email'])

        if len(records) > 0 :
            errors["email"] = "Account already exists for this email"

        return errors

    def login_validation(self, postData):
        errors = {}
        for thing in postData:
            if postData[thing] < 1:
                errors[thing] = "All fields required"
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"
        
        records = User.objects.filter(email=postData['email'])

        if len(records) > 0:
            pwd = records[0].password
            check = bcrypt.checkpw(postData['pwd'].encode(), pwd.encode())
            if check:
                return errors
            else:
                errors["pwd"] = "Incorrect user/password"
                return errors
        else:
            errors["email"] = "Account doesn't exist for this email. Please register."
            return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField(default=None)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User object: id='{}' first_name='{}' last_name='{}' birthdate='{}' email='{}' created='{}'>".format(self.id, self.first_name, self.last_name, self.birthdate, self.email, self.created_at)
