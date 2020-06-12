from django.shortcuts import render
#from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import UserRegistrationForm, UserForm
from django.urls import reverse, reverse_lazy #  импортируем reverse для смены адресс, а для переадреммации класса мы используем reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from .models import UserModel
from django.contrib import messages
from .decorators import  unauthenticated_user

@unauthenticated_user
def index(request):
    return render(request,'mainApp/index.html')

def home(request):
    return render(request,'mainApp/home.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username OR Password is incorrect")

    context = {}
    return render(request, 'registration/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('index')







    
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            user_inf = user_form.cleaned_data
            new_user.save()
            return render(request, 'registration/signup_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})

    
    




