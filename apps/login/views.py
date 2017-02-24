from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    print User.objects.all()
    if 'sessionID' in request.session:
        request.session.clear()
    return render(request, "login/index.html")

def login(request):
    if request.method == "POST":
        loginAttempt = User.objects.login(request.POST['loginUsername'],request.POST['loginPassword'])
        if loginAttempt[0]:
            request.session['sessionID'] = loginAttempt[1].id
            request.session['name'] = loginAttempt[1].name
            result = redirect('/home')
        else:
            messages.error(request, loginAttempt[1])
            result = redirect('/')
    else:
        result = redirect('/errorPage')

    return result

def registration(request):
    if request.method == "POST":
        x = User.objects.register(request.POST)
        if x[0]:
            messages.success(request, "Registered Successfully")
            request.session['sessionID'] = x[1].id
            request.session['name'] = x[1].name
            result = redirect('/home')
        else:
            print x[1]
            for error_message in x[1]:
                messages.error(request, error_message)
                result = redirect('/')
    else:
        result = redirect('/errorPage')

    return result


def home(request):
    if 'sessionID' not in request.session:
        result = redirect('/errorPage')
    else:
        print request.session['sessionID']
        user = User.objects.get(id = request.session['sessionID'])
        try:
            x = Trip.objects.exclude(Q(user_id= user) | Q(join_id=user))
            content = {
                'user_trips' : Trip.objects.filter(Q(user_id__id=request.session['sessionID']) | Q(join_id=user)),
                'all_trips' : x,
            }
            result = render(request, "login/success.html", content)
        except:
            result = redirect('/errorPage')

    # x = Trip.objects.exclude(user_id__id=request.session['sessionID'])
    # for each in x:
    #     print each.join_id.all()
    return result

def delete(request, id):
    if request.method == "POST":
        User.objects.get(id = id).delete()
        messages.error(request, "User deleted")
        return redirect('/')
    else:
        return redirect('/home')

def addTravel(request):
    print Trip.objects.all()
    return render(request, 'login/addTravel.html')

def processAddTravel(request):
    if request.method == 'POST':
        x = Trip.objects.addTravel(request.POST,request.session['sessionID'])
        if x[0]:
            messages.success(request, "Successfully Added Trip")
            result = redirect('/home')
        else:
            for error_message in x[1]:
                messages.error(request, error_message)
            result = redirect('/addTravel')
    return result

def destination(request,id):
    x = Trip.objects.get(id=id)
    content = {
    'trip' : x,
    'joined' : x.join_id.all()
    }
    return render(request, 'login/destination.html', content)
def join(request,id):
    x = Trip.objects.get(id = id)
    user = User.objects.get(id=request.session['sessionID'])
    x.join_id.add(user)
    print x.join_id.all()
    return redirect('/home')

def errorPage(request):
    return render(request, "login/getoutofhere.html")
