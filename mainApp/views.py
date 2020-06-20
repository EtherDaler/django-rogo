#from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import CreateUserForm, UserForm, RideForm, JoinForm, UserEditForm
from django.urls import reverse, reverse_lazy #  импортируем reverse для смены адресс, а для переадреммации класса мы используем reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from .models import UserModel, Rides, Join
from django.contrib import messages
from .decorators import  unauthenticated_user
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.db import transaction
from django.utils.translation import gettext as _

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



def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            UserModel.objects.create(
				user=user,
				)
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

@transaction.atomic
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Ваш профиль был успешно обновлен!'))
            return redirect('edit')
        else:
            messages.error(request, _('Пожалуйста, исправьте ошибки.'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserForm(instance=request.user.profile)
    return render(request, 'registration/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def def_phone():
     get_phone=UserForm.objects.get(phone)
     return get_phone
def def_car():
    get_car=UserForm.objects.get(user_car)
    return get_car
def def_car_year():
    get_car_year=UserForm.objects.get(user_car_year)
    return get_car_year
def def_car_number():
    get_car_number=UserForm.objects.get(user_car_number)
    return get_car_number

"""    
def register(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            user_inf = user_form.cleaned_data
            new_user.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = CreateUserForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})
"""

#Functions

def ridesList(request,*args,**kwargs):
    search_query = request.GET.get('search','')
    fail=False
    now = timezone.now()
    if search_query:
        listRides = Rides.objects.filter(Q(drop_location__icontains=search_query) )
    else:
        fail=True
        listRides = Rides.objects.filter(date__gte=now).order_by('date')
    search_query_pick = request.GET.get('search1','')
    if search_query_pick:
        listRides = Rides.objects.filter(pick_up_location__icontains=search_query_pick)
    else:
        listRides = Rides.objects.filter(date__gte=now).order_by('date')
    kwargs['list_rides'] = Rides.objects.filter(date__gte=now).order_by('date')
    context={ # через этот словарь можно передавать текст в html
   'listRides':listRides,
   'fail':fail,
    }
    return render(request,'rides/list.html',context)


#def ride_information(request, id):
 #   getRide =  Rides.objects.get(id = id) # так мы принимаем (наследуем только 1 параметр), а не все
  #  context = {
   #     'getRide':getRide,
    #    }
    #
    #return render(request,'rides/ride.html',context)

#def offerRide(request):
#    sucess = False
#    if request.method =='POST':   # проверяем передается ли форма
#        form = RideForm(request.POST) # мы получаем данные с браузера для обработки
#        if form.is_valid():  # проверка на валидацию
#            form.save()  # сохранение формы
#            sucess = True
#    context={
#        'list_rides':Rides.objects.all().order_by('id'),
#        'form':RideForm,
#        'sucess':sucess,
#        }
#
#   return render(request,'rides/create.html', context)


def updateRide(request,pk):
    get_ride = Rides.objects.get(pk=pk) 
    update = False
    if request.method =='POST':   # проверяем передается ли форма
        form = RideForm(request.POST,instance =  get_ride) # мы получаем данные с браузера для обработки
        if form.is_valid():  # проверка на валидацию
            form.save()  # сохранение формы
            update=True

    context={
        'get_ride': get_ride,
        'update':update,
        'form': RideForm(instance =  get_ride), # этот параметр делает так, чтобы поля которые мы меняем имели в качестве данных имеющуюся инфу
    }
    return render(request,'rides/updateRide.html',context)

def myRides(request):
    listRides = Rides.objects.all() # здесь мы наследуем БД 
    context={ # через этот словарь можно передавать текст в html
        'listRides':listRides,
    }
    return render(request,'rides/myRides.html',context)

def join_rides(request):
    listRides = Join.objects.all() # здесь мы наследуем БД 
    context={ # через этот словарь можно передавать текст в html
        'listRides':listRides,
    }
    return render(request,'rides/join_rides.html',context)

def deleteRide(request,pk):
    get_ride = Rides.objects.get(pk=pk)
    get_ride.delete() 
    return redirect(reverse('myRides'))

def deleteJoiner(request,pk):
    get_joiner = Join.objects.get(pk=pk)
    get_joiner.delete() 
    return redirect(reverse('Home'))

def contact(request):
    if request.method =="POST":
        form=request.POST.get(form)
        obj = model(pick_up_location=pick_up_location,drop_location=drop_location,total_rides=total_rides,date=date,car=car,car_number=car_number,car_year_issue=car_year_issue,phone_number=phone_number)
        obj.save()

def search(request):
    search_query = request.GET.get('search','')
    if search_query:
        rides = Rides.objects.filter(drop_location__icontains=search_query)
    else:
        rides = Rides.objects.all()




#Classes

class CustomSuccssMessageMixin:
    def success_msg(self):
        return False
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s'%(self.success_url,self.object.id)

#class HomeListView(ListView):
#    model = Rides
#    template_name = 'rides/list.html'
#    context_object_name = 'listRides'

class HomeDetailView(CustomSuccssMessageMixin,FormMixin,DetailView):
    model = Rides
    form_class = JoinForm
    template_name = 'rides/ride.html'
    context_object_name = 'getRide'
    success_msg = 'Вы присоединилтсь к поездке.'
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.ride = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    def get_success_url(self, **kwargs):
        return reverse_lazy('ride_page', kwargs={'pk':self.get_object().id})


class OfferRideCreateView(CustomSuccssMessageMixin,CreateView):
    model = Rides
    template_name = 'rides/create.html'
    form_class = RideForm
    success_url = reverse_lazy('offerRide')
    success_msg = 'Поездка создана'
    def get_context_data(self,**kwargs):
        kwargs['list_rides'] = Rides.objects.all().order_by('id')
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

#class LoginRequiredMixin(AccessMixin):
#    """Verify that the current user is authenticated."""
#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            return self.handle_no_permission()
#        return super().dispatch(request, *args, **kwargs)



#class RideUpdateView(UpdateView):
#    model = Rides
#    template_name = 'rides/updateRide.html'
#    form_class = RideForm
#    success_url = reverse_lazy('updateRide')
#    def get_context_data(self,**kwargs):
#        kwargs['update'] =  True
#        return super().get_context_data(**kwargs)
#        def get_form_kwargs(self):
#            kwargs = super().get_form_kwargs()
#            print(kwargs)
#        return kwargs

#class RideDeleteView(DeleteView):
#    model = Rides
#    template_name = 'rides/myRides.html'
#    success_url = reverse_lazy('myRides')
