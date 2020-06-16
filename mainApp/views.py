from django.shortcuts import render
#from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import CreateUserForm, UserForm
from django.urls import reverse, reverse_lazy #  импортируем reverse для смены адресс, а для переадреммации класса мы используем reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from .models import UserModel
from django.contrib import messages
from .decorators import  unauthenticated_user
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text

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
            messages.info(request, "Неправильное имя пользователя или пароль")

    context = {}
    return render(request, 'registration/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('index')

    
def register(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            # Save the User object
            user_inf = user_form.cleaned_data
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        user_form = CreateUserForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})

"""
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Подтвердите свой email.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            toemail = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[toemail])
            username = form.cleaned_data.get('username')
            email.send()

            return render(request, 'registration/signup_done.html')

            #messages.success(request, "Account was created for " + username)
            #return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
"""