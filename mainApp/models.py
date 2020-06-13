
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#class Profile(models.Model):
#    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
#    date_of_birth = models.DateField(blank=True, null=True)
#    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
#
#    def __str__(self):
#        return 'Profile for user {}'.format(self.user.username)
class UserModel(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='Телефон', max_length=200, null=True)
    #profile_pic = models.ImageField(null=True, blank=True, default="profile_1.png")
    user_car = models.CharField(verbose_name='Марка авто', null=True, max_length=200)
    user_car_year = models.CharField(verbose_name='Год выпуска автомобиля', null=True, max_length=200)
    user_car_number = models.CharField(verbose_name='Автомобильный номер', null=True, max_length=200)

    def __str__(self):
        return self.name


