from django.shortcuts import render

# Create your views here.
def main(request):
    print(request.user.is_authenticated)
    return render(request, "website/main.html")

def about(request):
    return render(request, "website/about.html")