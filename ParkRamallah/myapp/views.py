from django.shortcuts import render, redirect
from .forms import ReservationForm, UserRegisterForm, UserLoginForm
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required

# Users: Register page
# This function handles user registration 
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the form data to the database
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return JsonResponse({'success': True})  # Return success response
            else:
                return JsonResponse({'success': False, 'errors': 'Authentication failed'}, status=400)
        else:
            # If the form is not valid, return the errors in JSON format
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        # If there is an error in data we should stay in the form so the method will be get not post
        form = UserRegisterForm()
    return render(request, "register.html", {'form': form})

# Users: login page 
# This function renders the login page template
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True})  # Redirect then to the home page
                else:
                    return JsonResponse({'success': False, 'errors': 'Invalid username or password'}, status=400)
            except:
                return JsonResponse({'success': False, 'errors': 'User not exist'}, status=400)
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = UserLoginForm()
    return render(request, "login.html", {'form': form})

# Users: logout page 
# This function handles user logout
def logout_view(request):
    logout(request)
    return redirect('/login')

# Users: not login page 
# This function renders the not login page template
def not_login(request):
    return render(request,'not_logged_in.html')

# Users: Home page
# This function renders the home page template
@login_required(login_url='/not_login')
def home(request):
    parks = Park.objects.all()
    return render(request, 'home.html',{'parks': parks})


@login_required(login_url='/not_login')
def user_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    serialized_reservations = [{
        'id': reservation.id,
        'status': reservation.status,
        'parkNumber': reservation.parkNumber,
        'arrivalTime': reservation.arrivalTime.strftime('%Y-%m-%d %H:%M'),
        'departureTime': reservation.departureTime.strftime('%Y-%m-%d %H:%M'),
    } for reservation in reservations]  # Serialize reservations data
    return JsonResponse(serialized_reservations, safe=False)

def search_parks(request):
    location = request.GET.get('location')
    park_type = request.GET.get('type')  # Change variable name to park_type

    if location and park_type:
        parks = Park.objects.filter(location=location, park_type=park_type)  # Use park_type instead of type
    elif location:
        parks = Park.objects.filter(location=location)
    elif park_type:
        parks = Park.objects.filter(park_type=park_type)
    else:
        parks = Park.objects.all()

    serialized_parks = [{
        'name': park.name,
        'location': park.location,
        'type': park.park_type
    } for park in parks]  # Serialize parking data
    return JsonResponse(serialized_parks, safe=False)

def all_parks(request):
    parks = Park.objects.all()
    serialized_parks = serialized_parks = [{
        'name': park.name,
        'location': park.location,
        'type': park.park_type
    } for park in parks]  # Serialize parking data
    return JsonResponse(serialized_parks, safe=False)

# Users: Reservation page
# def reserve(request):
#     if request.method == 'POST':
#     # If the form has been submitted
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#                 # If the form data is valid, process the reservation
#                 # Here you can implement logic to save the reservation to the database
#                 # For now, we'll just redirect back to the reservation page
#                 form.save()
#                 return redirect('/home')  # Redirect to a success page
#         else:
#             # If it's a GET request, create a blank form
#             form = ReservationForm()

#         # Render the reservation page with the form
#         return render(request, 'reservation.html', {'form': form})
#     # current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')  # Format: YYYY-MM-DDTHH:MM
#     # context = {'current_datetime': current_datetime}
#     # if request.method == 'POST':
#     #     form = ReservationForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         # Redirect to a success page or home page
#     #         return redirect('/home')  # Replace 'home' with the URL name of your home page
#     # else:
#     #     form = ReservationForm()
#     # return render(request, 'reservation.html', {'form': form, **context})