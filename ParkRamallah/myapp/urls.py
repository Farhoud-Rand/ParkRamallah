from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view),
    path('login',views.login_view),
    path('register', views.register_view),
    path('home',views.home),
    path('reserve',views.reserve), 
    path('logout',views.logout_view),
]
