from django.contrib import admin
from .models import State, Volunteer, EndUser, Alert, Needs, StateCommittee


# Register your models here.

admin.site.register(State)
admin.site.register(Volunteer)
admin.site.register(EndUser)
admin.site.register(Alert)
admin.site.register(Needs)
admin.site.register(StateCommittee)
