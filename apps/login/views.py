from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    # User.objects.all().delete()
    # print User.objects.all()
    request.session.clear()
    return render(request, "login/index.html")

def login(request):
    if request.method == "POST":
        loginAttempt = User.objects.login(request.POST['loginEmail'],request.POST['loginPassword'])
        if loginAttempt[0]:
            request.session['sessionID'] = loginAttempt[1]
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
            request.session['sessionID'] = x[1]
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
    try:
        content = {
            'name' : User.objects.get(id=request.session['sessionID'])
        }
        result = render(request, "login/success.html", content)
    except:
        result = redirect('/errorPage')
    return result

def delete(request, id):
    if request.method == "POST":
        User.objects.get(id = id).delete()
        messages.error(request, "User deleted")
        return redirect('/')
    else:
        return redirect('/home')

def errorPage(request):
    return render(request, "login/getoutofhere.html")
