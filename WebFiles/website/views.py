from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, "website/main.html")

def about(request):
    return render(request, "website/about.html")