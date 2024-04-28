from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Reservation, Park
from django.forms import DateTimeInput
from django.core.exceptions import ValidationError
from datetime import timedelta
from django import forms
from django.utils import timezone
from datetime import datetime, timedelta

# Form to add new admin/user in admin panel
class AdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_staff', 'is_superuser')

# Form to add new parking in admin panel
class ParkAdminForm(forms.ModelForm):
    class Meta:
        model = Park
        exclude = ['created_at', 'updated_at']  

# Form to add new user in registration for users 
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Override widget attributes for form fields
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control p-2', 'placeholder': 'Username'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control p-2', 'placeholder': 'Email', 'required': True})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

# Form to login a user
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class': 'form-control p-2', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Password'}))

# Form to add new reservation for a user  
# class ReservationForm(forms.ModelForm):
#     class Meta:
#         model = Reservation
#         fields = ['park', 'start_time', 'end_time']
#         widgets = {
#             'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')
#         park = cleaned_data.get('park')

#         if start_time and end_time and park:
#             # Check if end time is greater than start time
#             if end_time <= start_time:
#                 raise forms.ValidationError("End time must be greater than start time.")
            
#             # Check if start time is in the past
#             if start_time <= timezone.now():
#                 raise forms.ValidationError("Start time cannot be in the past.")
            
#             # Check if there are any existing reservations for the selected park
#             existing_reservations = Reservation.objects.filter(
#                 park=park,
#                 start_time__lt=end_time,
#                 end_time__gt=start_time,
#                 status='active'  # Only consider active reservations
#             )

#             if existing_reservations.exists():
#                 raise forms.ValidationError("This time slot is already reserved.")
#         return cleaned_data

from django.utils import timezone

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, park_id=None, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.park_id = park_id

    class Meta:
        model = Reservation
        fields = ['date', 'start_time', 'duration']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        duration = cleaned_data.get('duration')
        park_id = self.park_id
        
        # Ensure date, start_time, and duration are provided
        if not date:
            raise forms.ValidationError("Date is required")
        if not start_time:
            raise forms.ValidationError("Start time is required")
        if not duration:
            raise forms.ValidationError("Duration is required")

        if date < timezone.now().date():
            raise forms.ValidationError("Selected date is in the past")

        # Convert duration to float
        duration_value = float(duration)

        # Combine date and start_time to create datetime object
        start_datetime = timezone.make_aware(datetime.combine(date, start_time))

        # Calculate end time
        end_datetime = start_datetime + timedelta(hours=duration_value)

        # Filter conflicting reservations
        conflicting_reservations = Reservation.objects.filter(
            park_id=park_id,
            date=date,
            start_time__lt=end_datetime.time(),
            start_time__gte=start_datetime.time()
        )
        if conflicting_reservations.exists():
            raise forms.ValidationError("Selected time slot is not available")

        return cleaned_data

