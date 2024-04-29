from django.shortcuts import render, redirect
from .forms import ReservationForm, UserRegisterForm, UserLoginForm, CommentForm
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
    # Update reservation status before sending to frontend
    update_reservation_status(reservations)
    serialized_reservations = models.Reservation.serialize_reservations(reservations)
    return JsonResponse(serialized_reservations, safe=False)

def update_reservation_status(reservations):
    current_time = timezone.now()

    for reservation in reservations:
        if reservation.status not in ['cancelled', 'expired']:
            start_datetime = datetime.combine(reservation.date, reservation.start_time)
            start_datetime = timezone.make_aware(start_datetime)  # Ensure start_datetime is timezone-aware
            duration_hours = float(reservation.duration)
            end_datetime = start_datetime + timedelta(hours=duration_hours)

            if end_datetime < current_time:
                reservation.status = 'expired'
                reservation.save()

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
            # logger.error("Form errors: %s", errors)  # Log form errors for debugging
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ReservationForm(park_id=park_id)
    return render(request, 'reservation.html', {'form': form, 'park': park})

from django.shortcuts import get_object_or_404

@login_required(login_url='/not_login')
def cancel_reservation(request, reservation_id):
    # Fetch the reservation object corresponding to the ID
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Update the reservation status to "cancelled"
    reservation.status = 'cancelled'
    reservation.save()

    return JsonResponse({'success': True, 'message': 'Reservation cancelled successfully'})

@login_required(login_url='/not_login')
def remove_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        # Check if the reservation exists and its status is expired or cancelled
        if reservation.status in ['expired', 'cancelled']:
            # Delete the reservation
            reservation.delete()
            return JsonResponse({'success': True, 'message': 'Reservation removed successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Reservation cannot be removed'})
    except Reservation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reservation not found'})


@login_required(login_url='/not_login')
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(models.Reservation, id=reservation_id)
    print("Reservation = ",reservation)
    start_time_choices = ReservationForm(instance=reservation).fields['start_time'].choices
    print("Time = ",start_time_choices)
    print("RT = ", reservation.start_time)
    
    duration_choices = ReservationForm(instance=reservation).fields['duration'].choices
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':

                return JsonResponse({'success': True})  # Return success response for AJAX request
            else:
                # Redirect to some success page for non-AJAX request
                # For example: return redirect('success_page')
                pass
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':

                return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Return form errors for AJAX request
            else:
                # Render the form again with errors for non-AJAX request
                pass
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation, 'start_time_choices': start_time_choices, 'duration_choices': duration_choices})


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Reservation
from decimal import Decimal


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

@login_required(login_url='/not_login')
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