from django.shortcuts import render, redirect
from .forms import ReservationForm, UserRegisterForm, UserLoginForm
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from . import models

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

# Users: Home page
# This function renders the home page template
def home(request):
    return render(request, "home.html")

# Users: logout page 
# This function handles user logout
def logout_view(request):
    logout(request)
    return redirect('/login')

# Users: Reservation page
def reserve(request):
    if request.method == 'POST':
    # If the form has been submitted
        form = ReservationForm(request.POST)
        if form.is_valid():
                # If the form data is valid, process the reservation
                # Here you can implement logic to save the reservation to the database
                # For now, we'll just redirect back to the reservation page
                form.save()
                return redirect('/home')  # Redirect to a success page
        else:
            # If it's a GET request, create a blank form
            form = ReservationForm()

        # Render the reservation page with the form
        return render(request, 'reservation.html', {'form': form})
    # current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')  # Format: YYYY-MM-DDTHH:MM
    # context = {'current_datetime': current_datetime}
    # if request.method == 'POST':
    #     form = ReservationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         # Redirect to a success page or home page
    #         return redirect('/home')  # Replace 'home' with the URL name of your home page
    # else:
    #     form = ReservationForm()
    # return render(request, 'reservation.html', {'form': form, **context})