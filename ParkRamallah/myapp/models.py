from django.db import models
from django.contrib.auth.models import User

# Parking lot table 
class Park(models.Model):
    TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('special', 'Special Needs'),
    ]
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    park_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Function to return all parking information
    @classmethod
    def get_all_parkings(cls): 
        return cls.objects.all()
    
    # Function to get a parking by its ID and return its information
    @classmethod
    def get_park_by_id(cls,id): 
        return cls.objects.get(id=id)
    
    # Function to fillter parkings according to search 
    @classmethod
    def search_result(cls, data):
        park_location = data.GET.get('location')
        park_type = data.GET.get('type')
        park_name = data.GET.get('name')  
        parks = cls.get_all_parkings()
        # Filter parks based on location, type, and park name
        if park_location:
            parks = parks.filter(location=park_location)
        if park_type:
            parks = parks.filter(park_type=park_type)
        if park_name:
            parks = parks.filter(name=park_name)
        return parks

    # # Function to get parking information as a list of dictionaries
    @classmethod
    def serialize_parks(cls, parks):
        serialized_parks = [{
            'name': park.name,
            'location': park.location,
            'type': park.park_type,
            'id' : park.id,
        } for park in parks]
        return serialized_parks

# Reservation table (inner table between Park and User tables)
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reservations', null=True)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, related_name='park_reservations', null=True)
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.DecimalField(max_digits=3, decimal_places=1)  # in hours
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    total_price = models.FloatField(default=0.0)
    car_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Function to get all user reservations 
    @classmethod
    def get_user_reservations(cls, user):
        return cls.objects.filter(user=user)

    # Function to get all reservations information as a list of dictionaries
    @classmethod
    def serialize_reservations(cls, reservations):
        serialized_reservations = [{
            'id': reservation.id,
            'status': reservation.status,
            'park': reservation.park.id,
            'start_time': reservation.start_time.strftime('%H:%M'),
            'duration': reservation.duration,
            'car_number':reservation.car_number,
        } for reservation in reservations]
        return serialized_reservations

    # Function to get a specific reservation by ID
    @classmethod
    def get_reservation_by_id(cls, id):
        return cls.objects.get(id)

# Comment table (has a relation one to many with user table)
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
###################################################################
    
 
