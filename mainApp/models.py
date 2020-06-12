
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
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, )
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(null=True, max_length=200)
    #profile_pic = models.ImageField(null=True, blank=True, default="profile_1.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    user_first_name = models.CharField(null=True, max_length=200)
    user_last_name = models.CharField(null=True, max_length=200)
    user_car = models.CharField(null=True, max_length=200)
    user_car_year = models.CharField(null=True, max_length=200)
    user_car_number = models.CharField(null=True, max_length=200)

    def __str__(self):
        return self.name


