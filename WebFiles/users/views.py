from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def login(request):
    if request.method == 'POST':
        print('Message received')
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def logout(request):
    return HttpResponseRedirect(reverse("webpage:main"), {
        'message': 'Logged out successfully!'
    })