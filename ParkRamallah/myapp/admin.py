from django.contrib import admin
from .models import Park, Reservation, Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import AdminCreationForm
from .forms import ParkAdminForm

# Register the DB table in admain panel
admin.site.register(Reservation)
admin.site.register(Comment)

class CustomUserAdmin(UserAdmin):
    add_form = AdminCreationForm
    # Customize the fields to be displayed when adding a new user
    search_fields = ['username','id'] # Allow search by these fields 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register User with the customized UserAdmin
admin.site.register(User, CustomUserAdmin)

class ParkAdmin(admin.ModelAdmin):
    form = ParkAdminForm
    search_fields = ['id','location','name']

    list_display = ['id','name','location', 'park_type','created_at','updated_at']

# Register Park with the custom ParkAdmin
admin.site.register(Park, ParkAdmin)