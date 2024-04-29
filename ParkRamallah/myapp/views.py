from django.shortcuts import render, redirect
from .forms import ReservationForm, UserRegisterForm, UserLoginForm
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from . import models
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
    parks = models.Park.get_all_parkings()
    return render(request, 'home.html',{'parks': parks})

# This function returns user reservations as json response
@login_required(login_url='/not_login')
def user_reservations(request):
    reservations = models.Reservation.get_user_reservations(request.user)
    serialized_reservations = models.Reservation.serialize_reservations(reservations)
    return JsonResponse(serialized_reservations, safe=False)

# This function returns result of search as json response
@login_required(login_url='/not_login')
def search_parks(request):
    parks = models.Park.search_result(request)
    serialized_parks = models.Park.serialize_parks(parks)
    return JsonResponse(serialized_parks, safe=False)

# This function returns all parks information as json response
@login_required(login_url='/not_login')
def all_parks(request):
    parks = models.Park.get_all_parkings()
    serialized_parks = models.Park.serialize_parks(parks)
    return JsonResponse(serialized_parks, safe=False)

# Users: Reservation page
from decimal import Decimal

# @login_required(login_url='/not_login')
# def reserve(request, park_id):
#     try:
#         park = models.Park.objects.get(id=park_id)
#     except models.Park.DoesNotExist:
#         return JsonResponse({'success': False, 'errors': 'Park does not exist.'}, status=400)

#     if request.method == 'POST':
#         form = ReservationForm(request.POST, park_id=park_id)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.user = request.user
#             reservation.park = park
#             reservation.status = 'active'
#             reservation.total_price = 10 * float(form.cleaned_data['duration'])
#             reservation.save()
#             return JsonResponse({'success': True, 'message': 'Reservation successfully made!'})
#         else:
#             errors = form.errors
#             return JsonResponse({'success': False, 'errors': errors}, status=400)
#     else:
#         form = ReservationForm(park_id=park_id)
#     return render(request, 'reservation.html', {'form': form, 'park': park})

from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='/not_login')
def reserve(request, park_id):
    try:
        park = models.Park.objects.get(id=park_id)
    except models.Park.DoesNotExist:
        return JsonResponse({'success': False, 'errors': 'Park does not exist.'}, status=400)

    if request.method == 'POST':
        form = ReservationForm(request.POST, park_id=park_id)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            start_time = form.cleaned_data.get('start_time')
            duration = form.cleaned_data.get('duration')
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.park = park
            reservation.status = 'active'
            reservation.total_price = 10*float(duration)
            reservation.save()
            return JsonResponse({'success': True, 'message': 'Reservation successfully made!'})
        else:
            errors = form.errors
            logger.error("Form errors: %s", errors)  # Log form errors for debugging
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ReservationForm(park_id=park_id)
    return render(request, 'reservation.html', {'form': form, 'park': park})

@login_required(login_url='/not_login')
def cancel_reservation(request, reservation_id):
    try:
        reservation = models.Reservation.objects.get(pk=reservation_id)
    except models.Reservation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reservation not found'}, status=404)
    
    # Update the reservation status to "cancelled"
    reservation.status = 'cancelled'
    reservation.save()

    return JsonResponse({'success': True, 'message': 'Reservation cancelled successfully'})


# Define a view to handle updating reservation status to "expired"
def expire_reservation(request, reservation_id):
    try:
        reservation = models.Reservation.objects.get(pk=reservation_id)
    except models.Reservation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reservation not found'}, status=404)
    
    if reservation.status != 'expired' and reservation.status != 'cancelled': #and reservation.end_time < timezone.now():
        reservation.status = 'expired'
        reservation.save()
        return JsonResponse({'success': True, 'message': 'Reservation expired successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Reservation already expired or cancelled'})
    

@login_required(login_url='/not_login')
def edit_reservation(request, reservation_id):
    try:
        reservation = models.Reservation.objects.get(pk=reservation_id)
    except models.Reservation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reservation not found'}, status=404)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Reservation updated successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ReservationForm(instance=reservation)
        if reservation.status == 'active':
            # Render the edit_reservation.html template with the form and reservation details
            return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})
        else:
            # If the reservation status is not "active", do not show the edit page
            return JsonResponse({'success': False, 'message': 'Reservation is not active'}, status=400)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Reservation
from decimal import Decimal

@receiver(post_save, sender=Reservation)
def update_reservation_status(sender, instance, **kwargs):
    if instance.status != 'cancelled' and instance.status != 'expired':  
        start_datetime = timezone.make_aware(datetime.combine(instance.date, instance.start_time))
        duration_float = float(instance.duration)  # Convert Decimal to float
        end_datetime = start_datetime + timedelta(hours=duration_float)
        if end_datetime < timezone.now():
            instance.status = 'expired'
            instance.save()
    
@login_required(login_url='/not_login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Update the user's information
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request,username=username, password=password)
            if user is not None:
                return JsonResponse({'success': True})  # Return success response
            else:
                return JsonResponse({'success': False, 'errors': 'Authentication failed'}, status=400)
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = UserRegisterForm(instance=user)  # Pre-fill the form with user's data
    
    return render(request, "profile.html", {'form': form})

def about_us_view(request):
    return render(request, "about_us.html")

from .forms import CommentForm

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Assuming you're using Django's built-in User model
            comment.save()
            return redirect('home')  # Redirect to the home page or wherever you want
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})