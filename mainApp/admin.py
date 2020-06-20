from django.contrib import admin
from .models import UserModel,Rides,Join

admin.site.register(Rides)

admin.site.register(Join)

admin.site.register(UserModel)
