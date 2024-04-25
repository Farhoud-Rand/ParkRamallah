from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view),
    path('login',views.login_view),
    path('register', views.register_view),
    # path('reserve',views.reserve), 
    path('logout',views.logout_view),
    path('not_login',views.not_login),
    path('home', views.home, name='home'),
    path('user/reservations/', views.user_reservations, name='user_reservations'),
    path('search/', views.search_parks, name='search_parks'),
    path('all_parks/', views.all_parks, name='all_parks'),
]
