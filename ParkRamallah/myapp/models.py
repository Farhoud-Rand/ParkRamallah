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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Reservation table (inner table between Park and User tables)
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reservations', null=True)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, related_name='park_reservations', null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Comment table (has a relation one to many with user table)
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)