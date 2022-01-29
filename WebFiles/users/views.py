from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from django.contrib.auth.models import User
from .custom import *

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:user"))
    return render(request, 'users/login.html')

def register(request):
    if request.method == "POST":
        passwd = request.POST["password"]
        cpasswd = request.POST["cpassword"]
        if not (passwd == cpasswd):
            return render(request, 'users/register.html', {
                'error': "Passwords don't match",
                # If possible, return data
            })
        else:
            username = request.POST["username"]
            users = User.objects.all()
            # Conditional to check if username is already taken or not
            if username in [i.username for i in users]:
                return render(request, 'users/register.html', {
                    'error': 'Username already taken'
                })
            else:
                # Collecting left out data
                firstname = request.POST["firstname"]
                lastname = request.POST["lastname"]
                email = request.POST["email"]
                
                # Creating user
                user = User.objects.create_user(username=username,
                                                password=passwd,
                                                first_name=firstname,
                                                last_name=lastname,
                                                email=email)
                
                # Logging in the user
                loginuser(request, user)

                # Getting user alarms
                alarms = request.user.alarms.all()
                return render(request, 'users/user.html', {
                    'alarms': alarms,
                })

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:user"))
    return render(request, 'users/register.html')

def logout(request):
    LOGGED_IN = False
    logoutuser(request)
    return render(request, "website/main.html", {
        'message': 'Logged out successfully!'
    })

def user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        # Checking if entered credentials are right
        if user is not None:
            loginuser(request, user)
            # Getting user alarms
            alarms = request.user.alarms.all()
            return render(request, 'users/user.html', {
                'alarms': alarms,
                'youngest': calculate(alarms)
            })
        return render(request, "users/login.html", {
            'failed_msg': 'Invalid Credentials'
        })

    # If user entered tab without logging in
    elif not request.user.is_authenticated:
        return render(request, "users/login.html")
    else:
        # Getting user alarms
        alarms = request.user.alarms.all()
        return render(request, 'users/user.html', {
            'alarms': alarms,
            'youngest': calculate(alarms)
        })

def edit(request):
    if not request.user.is_authenticated:
        return render(request, 'website/main.html')
    else:
        alarms = request.user.alarms.all()
        if alarms is not None:
            return render(request, 'users/edit.html', {
                'alarms': alarms,
            })
        else:
            return render(request, 'users/edit.html', {
                'number': [i for i in range(1, 5)],
            })

def edituser(request):
    if request.method == 'POST':
        passwd = request.POST["password"]
        cpasswd = request.POST["cpasswd"]
        print(f"Passwords: {passwd}, {cpasswd}")

        if passwd != cpasswd:
            return render(request, 'users/edit.html', {
                'usererror': "Password and Confirm password don't match",
            })
        else:
            username = request.POST["username"]
            print(f"New Username: {username}")
            try:
                user = User.objects.get(username=username)
            except:
                pass
            else:
                return render(request, 'users/edit.html', {
                    'usererror': "Username already exists",
                })
                
                user = User.objects.get(username=username)
                for key, value in request.POST.items():
                    if value not in ['', 'cpasswd']:
                        setattr(user, key, value)
                print(f"Username: {user.username}\nFirstname: {user.first_name}\nLastname: {user.last_name}")
