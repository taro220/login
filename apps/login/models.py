from __future__ import unicode_literals
import bcrypt
from django.db import models
import datetime
# from ..secretPost import Secret, Likes
import re
# Create your models here.
def checkDate(first,second):
    date_error = True
    if first[0] > second[0]: #if start year is passed
        date_error = False
    elif first[0] == second[0]: #if start year is the same then
        if first[1] > second[1]: #same year current month passed
            date_error = False
        elif first[1] == second[1]:#same year same month
            if first[2] > second[2]: # current day passed
                date_error = False
    return date_error

# def checkDateOverlap(s,e,check):
#     date_e = True
#     s = str(s)
#     s = s.split(" ")
#     s = s[0].split("-")
#     e = str(e)
#     e = e.split(" ")
#     e = e[0].split("-")
#     if checkDate(s,check): #date after start
#         print "start is after check"
#         if checkDate(check,e): #date is before end
#             print "end is after check"
#             date_e = False
#     return date_e

    # print "start {}".format(s)
    # print "end {}".format(e)

class UserManager(models.Manager):
    def register(self, formPostData):
        errors = []
        no_errors = True
        username_regex= r"(^[a-zA-Z0-9_.+-]{3,}$)"
        name_regex= r"(^[a-zA-Z]{3,} [a-zA-Z]{3,}$)"
        password_regex= r"(^[a-zA-Z0-9_.+-]{8,}$)"
        if not re.match(name_regex, formPostData['name']):
            errors.append("Invalid Name. Require Full Name")
            no_errors = False
        # if not re.match(name_regex, formPostData['l_name']):
        #     errors.append("Last Name Invalid")
        #     no_errors = False
        if not re.match(username_regex, formPostData['username']):
            errors.append("User Name Invalid. Only letters and nummbers. At least 3 characters")
            no_errors = False
        else:
            if User.objects.filter(username = formPostData['username'].lower()):
                errors.append("Username already in use")
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
            x = User.objects.create(name = formPostData['name'].lower(), username = formPostData['username'].lower(), password = hashed)
            results = no_errors, x
        else:
            results = no_errors, errors

        return results

    def login(self, username, password):
        try:
            user = User.objects.get(username = username.lower())
            if bcrypt.checkpw(password.encode(encoding="utf-8", errors="strict"), user.password.encode(encoding="utf-8", errors="strict")):
                result = True, user
            else:
                result = False, "Password does not match"
        except:
            result = False, "Invalid Username"
        return result

class TripManager(models.Manager):

    def addTravel(self, travelPostData, id):
        errors = []
        no_errors = True
        start = travelPostData['start_date'].split('-')
        end = travelPostData['end_date'].split('-')
        curr = datetime.datetime.now().strftime("%Y %m %d").split(" ")
        if len(travelPostData['destination']) <= 0:
            no_errors = False
            errors.append("Destination cannot be blank")
        if len(travelPostData['description']) <= 0:
            no_errors = False
            errors.append("Description cannot be blank")
        if start[0] == '':
            errors.append("Start Date cannot be empty")
            no_errors = False
        else:
            if checkDate(curr,start) == False:
                errors.append("Start date must be after current date")
                no_errors = False
        if end[0] == '':
            errors.append("End Date cannot be empty")
            no_errors = False
        else:
            if checkDate(start,end) == False:
                errors.append("End date must be after start date")
                no_errors = False
        if start == end:
            errors.append("Warning! Start and End date are the same")

        if no_errors == True:
            user = User.objects.get(id=id)
            start = "-".join(start)
            end = "-".join(end)

            if Trip.objects.filter(dest_stand = travelPostData['destination'].lower(), start_date = start, end_date = end):
                no_errors = False
                errors.append("Trip already exsist")

            user_trips = Trip.objects.filter(user_id= user)

            # for aTrip in user_trips:
            #     if checkDateOverlap(aTrip.start_date,aTrip.end_date,start):
            #         if checkDateOverlap(aTrip.start_date,aTrip.end_date,end):
            #             print "OverLap"
            #     else:
            #         print "OK"
        if no_errors == True:
            Trip.objects.create(destination = travelPostData['destination'],\
             description = travelPostData['description'], start_date = start, end_date = end,\
             user_id = user, dest_stand = travelPostData['destination'].lower())

        # print start, end, curr
        return no_errors, errors




class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
    def __str__(self):
        return "First Name: {}, username {}, Password: {}\n".format(self.name,self.username,self.password)


class Trip(models.Model):
    destination = models.CharField(max_length=100)
    dest_stand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=1000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    user_id = models.ForeignKey(User, related_name = "planner")
    join_id = models.ManyToManyField(User, related_name = "joined_user", blank = True, null = True)
    objects = TripManager()
    def __str__(self):
        return "Destination: {}, user: {}".format(self.destination, self.user_id.name)
