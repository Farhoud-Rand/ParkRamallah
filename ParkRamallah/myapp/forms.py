from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Reservation, Park
from django.forms import DateTimeInput
from django.core.exceptions import ValidationError

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
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['park', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        park = cleaned_data.get('park')

        if start_time and end_time and park:
            # Check if end time is greater than start time
            if end_time <= start_time:
                raise forms.ValidationError("End time must be greater than start time.")
            
            # Check if start time is in the past
            if start_time <= timezone.now():
                raise forms.ValidationError("Start time cannot be in the past.")
            
            # Check if there are any existing reservations for the selected park
            existing_reservations = Reservation.objects.filter(
                park=park,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status='active'  # Only consider active reservations
            )

            if existing_reservations.exists():
                raise forms.ValidationError("This time slot is already reserved.")
        return cleaned_data