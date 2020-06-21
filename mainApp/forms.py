from django import forms
from django.contrib.auth.models import User
from .models import UserModel, Rides, Join
from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('phone', 'avatar', 'user_car', 'user_car_year', 'user_car_number')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError(_('This email already exists'))
        return email


class RideForm(forms.ModelForm):
    class Meta:
        model=Rides
        fields = ('pick_up_location','drop_location','total_rides','luggage','date','time','car','car_number','car_year_issue','price','phone_number')
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
