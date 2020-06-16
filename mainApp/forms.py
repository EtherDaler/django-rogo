from django import forms
from django.contrib.auth.models import User
from .models import UserModel
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ('phone', 'user_car', 'user_car_year', 'user_car_number')
        exclude = ['user']

class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
    
    def cleaned_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Такой Электронный адрес уже используется.')
        return email