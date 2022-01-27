from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from django.contrib.auth.models import User

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
                return render(request, 'users/user.html')

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
            return render(request, "users/user.html")
        return render(request, "users/login.html", {
            'failed_msg': 'Invalid Credentials'
        })

    # If user entered tab without logging in
    elif not request.user.is_authenticated:
        print('Not logged in')
        return render(request, "users/login.html")
    else:
        return render(request, "users/user.html")