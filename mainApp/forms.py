from django import forms
from django.contrib.auth.models import User
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ('phone', 'user_car', 'user_car_year', 'user_car_number')
        exclude = ['user']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError(_('This email already exists'))
        return email