from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_view
from django.views.generic import ListView, DetailView
from .models import Rides

urlpatterns = [
    path('', views.index, name="index"),


    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('home/',views.home,name='home'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('reset_password/', auth_view.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_complete'),

    #path('',views.ridesList, name="ridesList"),
    path('list/',views.ridesList,name='Home'),
    #path('<int:id>',views.ride_information, name="ride_information") # <int:id> добавляет отдельный айди для каждой поездки
    path('<int:pk>/',views.HomeDetailView.as_view(),name='ride_page'),
    path('offerRide/',views.OfferRideCreateView.as_view(),name='offerRide'),
    path('updateRide/<int:pk>',views.updateRide,name='updateRide'),
    path('myRides/',views.myRides,name='myRides'),
    path('deleteRide/<int:pk>/',views.deleteRide,name='deleteRide'),
    path('join_rides/', views.join_rides ,name='join_rides'),
    path('deleteJoiner/<int:pk>/',views.deleteJoiner,name='deleteJoiner'),

    path('edit/', views.edit, name='edit'),
]

