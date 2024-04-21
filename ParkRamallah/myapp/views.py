from django.shortcuts import render

# Users: login page 
def login(request):
    return render(request,"login.html")
