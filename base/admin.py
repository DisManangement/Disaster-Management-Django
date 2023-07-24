from django.contrib import admin
from .models import State, Volunteer, EndUser


# Register your models here.

admin.site.register(State)
admin.site.register(Volunteer)
admin.site.register(EndUser)
