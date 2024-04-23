from django.shortcuts import render

# Users: login page 
def login(request):
    return render(request,"login.html")

# Users: Register page 
def register(request):
    return render(request,"register.html")

# Users: Home page
def home(request):
    return render(request, "home.html")
