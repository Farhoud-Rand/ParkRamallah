from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view),
    path('login/', views.login_view, name='login'),
    path('register', views.register_view),
    path('reserve/<int:park_id>/', views.reserve, name='reserve'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('expire_reservation/<int:reservation_id>/', views.expire_reservation, name='expire_reservation'),
    path('edit_reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('logout',views.logout_view),
    path('not_login',views.not_login),
    path('home', views.home, name='home'),
    path('user/reservations/', views.user_reservations, name='user_reservations'),
    path('search/', views.search_parks, name='search_parks'),
    path('all_parks/', views.all_parks, name='all_parks'),
    path('profile/', views.profile_view, name='profile'),
    path('about_us',views.about_us_view),
    path('add_comment',views.add_comment),
]
