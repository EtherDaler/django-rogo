from django.conf.urls import url
from django.urls import path
from django.views.generic import ListView, DetailView
from rides.models import Rides
from . import views

urlpatterns = [
    #path('',views.ridesList, name="ridesList"),
    path('',views.ridesList,name='Home'),
    #path('<int:id>',views.ride_information, name="ride_information") # <int:id> добавляет отдельный айди для каждой поездки
    path('<int:pk>/',views.HomeDetailView.as_view(),name='ride_page'),
    path('offerRide/',views.OfferRideCreateView.as_view(),name='offerRide'),
    path('updateRide/<int:pk>',views.updateRide,name='updateRide'),
    path('myRides/',views.myRides,name='myRides'),
    path('deleteRide/<int:pk>/',views.deleteRide,name='deleteRide'),
    path('join_rides/',views.join_rides,name='join_rides')
]