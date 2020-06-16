from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name="index"),


    path('register/', views.register, name="register"),
    path('login/', views.login_page, name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('home/',views.home,name='home'),
    #path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('reset_password/', auth_view.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_complete'),


]