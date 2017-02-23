from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):
    def register(self, formPostData):
        errors = []
        no_errors = True
        email_regex= r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        name_regex= r"(^[a-zA-Z]{2,}$)"
        password_regex= r"(^[a-zA-Z0-9_.+-]{8,}$)"
        if not re.match(name_regex, formPostData['f_name']):
            errors.append("First Name Invalid")
            no_errors = False
        if not re.match(name_regex, formPostData['l_name']):
            errors.append("Last Name Invalid")
            no_errors = False
        if not re.match(email_regex, formPostData['email']):
            errors.append("Invalid Email")
            no_errors = False
        else:
            if User.objects.filter(email = formPostData['email'].lower()):
                errors.append("Email already in use")
                no_errors = False
        if not re.match(password_regex, formPostData['password']):
            errors.append("Invalid Password")
            no_errors = False
        else:
            if not formPostData['password'] == formPostData['c_password']:
                errors.append("Password does not match")
                no_errors = False
        if no_errors:
            hashed = bcrypt.hashpw(formPostData['password'].encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
            x = User.objects.create(f_name = formPostData['f_name'].lower(), l_name = formPostData['l_name'].lower(), email = formPostData['email'].lower(), password = hashed)
            results = no_errors, x.pk
        else:
            results = no_errors, errors

        return results

    def login(self, email, password):
        try:
            user = User.objects.get(email = email.lower())
            if bcrypt.checkpw(password.encode(encoding="utf-8", errors="strict"), user.password.encode(encoding="utf-8", errors="strict")):
                result = True, user.id
            else:
                result = False, "Password does not match"
        except:
            result = False, "Invalid Email"
        return result



class User(models.Model):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
    def __str__(self):
        return "First Name: {}, Last Name: {}, Email {}, Password: {}\n".format(self.f_name,self.l_name,self.email,self.password)
