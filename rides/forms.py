from django import forms
from .models import Rides, Join
from django.contrib.auth.models import User
from django.forms import ModelForm


class RideForm(forms.ModelForm):
    class Meta:
        model=Rides
        fields = ('pick_up_location','drop_location','total_rides','date','time','car','car_number','car_year_issue','price','phone_number')
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class JoinForm(forms.ModelForm):
   class Meta:
        model=Join
        fields = ('author_phone',)
   def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


   

