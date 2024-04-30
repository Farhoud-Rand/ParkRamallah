from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Reservation, Park, Comment
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

# Form to reserve a parking lot
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'start_time', 'duration','car_number']
    
    choices_for_start_time = []
    choices_for_duration = []

    def __init__(self, *args, park_id=None, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.park_id = park_id
        
        # Get current time
        current_time = datetime.now().replace(second=0, microsecond=0)

        # Generate choices for the next 24 hours in 30-minute intervals starting from the next half hour
        if not self.choices_for_start_time:
            next_time = current_time + timedelta(minutes=(30 - current_time.minute % 30))
            for _ in range(48):  # 48 half-hour intervals cover 24 hours
                time_str = next_time.strftime('%H:%M')  # Format as '09:00'
                time_str = time_str.lstrip('0')  # Remove leading zeros from hours
                self.choices_for_start_time.append((time_str, time_str))
                next_time += timedelta(minutes=30)

        # Create the ChoiceField for start time
        self.fields['start_time'] = forms.ChoiceField(
            choices=self.choices_for_start_time, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        # Generate choices for durations from 30 minutes to 6 hours
        if not self.choices_for_duration:
            self.choices_for_duration = [
                (0.5, '30 minutes'),
                (1, '1 hour'),
                (1.5, '1.5 hours'),
                (2, '2 hours'),
                (2.5, '2.5 hours'),
                (3, '3 hours'),
                (3.5, '3.5 hours'),
                (4, '4 hours'),
                (4.5, '4.5 hours'),
                (5, '5 hours'),
                (5.5, '5.5 hours'),
                (6, '6 hours'),
            ]

        # Create the ChoiceField for duration
        self.fields['duration'] = forms.ChoiceField(
            choices=self.choices_for_duration, 
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        self.fields['car_number'].widget.attrs['class'] ='form-control'    

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        duration = cleaned_data.get('duration')
        car_number = cleaned_data.get('car_number')
        park_id = self.park_id
        
        # Ensure date, start_time, duration and car_number are provided
        if not date:
            raise forms.ValidationError("Date is required")
        if not start_time:
            raise forms.ValidationError("Start time is required")
        if not duration:
            raise forms.ValidationError("Duration is required")
        if not car_number:
            raise forms.ValidationError("Car Number is required")

        if date < timezone.now().date():
            raise forms.ValidationError("Selected date is in the past")
    
        # Convert duration to float
        duration_value = float(duration)

        # Calculate start datetime
        start_datetime = datetime.combine(date, datetime.strptime(start_time, '%H:%M').time())

        # Calculate end datetime
        end_datetime = start_datetime + timedelta(hours=duration_value)

        # Filter conflicting reservations
        conflicting_reservations = Reservation.objects.filter(
            park_id=park_id,
            date=date,
            start_time__lt=end_datetime.time(),
            start_time__gte=start_datetime.time()

        )
        if conflicting_reservations.exists():
            raise forms.ValidationError("This time slot is already reserved")
        return cleaned_data

# Form to add new comment and send it to admins
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter content'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if not title:
            self.add_error('title', "Title cannot be empty.")
        if not content:
            self.add_error('content', "Content cannot be empty.")

        return cleaned_data

# Form to update user profile
class UpdateProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        # Override widget attributes for form fields
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control p-2', 'placeholder': 'Username'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control p-2', 'placeholder': 'Email', 'required': True})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise forms.ValidationError("This email is already registered")
        return email

# Form to update user password
class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        # Override widget attributes for form fields
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Password'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control p-2', 'placeholder': 'Confirm Password'})

