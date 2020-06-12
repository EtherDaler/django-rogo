from django import forms
from django.contrib.auth.models import User
from .models import UserModel
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        exclude = ['user']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']