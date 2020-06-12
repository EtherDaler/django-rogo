from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Rides, Join
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import RideForm, JoinForm
from django.urls import reverse, reverse_lazy #  импортируем reverse для смены адресс, а для переадреммации класса мы используем reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.db.models import Q

#Functions

def ridesList(request,*args,**kwargs):
    search_query = request.GET.get('search','')
    fail=False
    if search_query:
        listRides = Rides.objects.filter(Q(drop_location__icontains=search_query) | Q(pick_up_location__icontains=search_query))
    else:
        fail=True
        listRides = Rides.objects.all().order_by('date_create')
    #search_query_pick = request.GET.get('search_pick','')
    #if search_query_pick:
    #    listRides = Rides.objects.filter(pick_up_location__icontains=search_query_pick)
    #else:
    #    listRides = Rides.objects.all()
    kwargs['list_rides'] = Rides.objects.all().order_by('date_create')
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
    return redirect(reverse('ride_page'))

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




