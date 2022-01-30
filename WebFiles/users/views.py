from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from django.contrib.auth.models import User
from .custom import *
from users.models import Alarm

# Create your views here.
def login(request):
    print("login")
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:user"))
    return render(request, 'users/login.html')

def register(request):
    ''' Function to register user '''

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
    return render(request, "website/main.html")

def user(request):
    ''' Display user webpage '''

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
    ''' Function to display webpage for user edit '''
    
    if not request.user.is_authenticated:
        return render(request, 'website/main.html')
    else:
        alarms = request.user.alarms.all()
        length = int(len(alarms))
        print(length != 0)
        if length != 0:
            left = [i for i in range(length+1, 6 - length)]
            print(left)
            return render(request, 'users/edit.html', {
                'alarms': alarms,
                'left': left,
            })
        else:
            return render(request, 'users/edit.html', {
                'alarms': [],
                'left': [i for i in range(1, 5)],
            })

def edituser(request):
    ''' Function to edit details of user '''

    if request.method == 'POST':
        passwd = request.POST["password"]
        cpasswd = request.POST["cpasswd"]
        print(f"Passwords: {passwd}, {cpasswd}")

        if passwd != cpasswd:
            alarms = request.user.alarms.all()
            return render(request, 'users/edit.html', {
                'usererror': "Password and Confirm password don't match",
                'alarms': alarms,
            })
        else:
            username = request.POST["username"]
            try:
                user = User.objects.get(username=username)
            except:
                user = User.objects.get(username=request.user.username)
                for key, value in list(request.POST.items())[1:]:
                    if value not in ['', 'cpasswd']:
                        setattr(user, key, value)
                user.save()
                return HttpResponseRedirect(reverse('users:user'))
            else:
                alarms = request.user.alarms.all()
                if alarms is not None:
                    return render(request, 'users/edit.html', {
                        'alarms': alarms,
                        'usererror': "Username already exists"
                    })
    else:
        return HttpResponseRedirect(reverse('users:user'))

def editalarms(request):
    ''' Function to edit alarms of user '''

    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        alarms = Alarm.objects.filter(user=user)
        print(request.POST)
        try:
            alarm = alarms.get(name=request.POST["alarms"])
        except:
            alarm = Alarm(user_id=request.user.id, name=request.POST["name"], medname=(request.POST["medname"]), time=(request.POST["time"]))
        else:
            alarm.name = request.POST["name"]
            alarm.time = request.POST["time"]
            alarm.medname = request.POST["medname"]
        

        alarm.save()
        return HttpResponseRedirect(reverse('users:user'))

        '''
        # Editing existing alarms
        for i in range(len(alarms)):
            for key, value in request.POST.items():
                if value != '':
                    print(f"{key}, {value}")
                    # setattr(alarms[i], key, value)
                alarms[i].save()
        return HttpResponseRedirect(reverse("users:user"))
        '''
            
    else:
        return HttpResponseRedirect(reverse('users:user'))