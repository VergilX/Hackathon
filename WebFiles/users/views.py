from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser

LOGGED_IN = False
'''
Notes
- In this case, you've gotta use `if request.user.is_authenticated` in 3 functions. Instead,
   if you can remove the tabs of LOGIN and REGISTER in webpage using LOGGED_IN/request.user.is_authenticated, it would be nice
'''

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:user"))
    return render(request, 'users/login.html')

def register(request):
    if request.user.is_authenticated:
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
        print('sent data')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        # Checking if entered credentials are right
        if user is not None:
            loginuser(request, user)
            LOGGED_IN = True
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