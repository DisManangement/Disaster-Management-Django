from django.urls import path
from . import views


urlpatterns= [
    path('', views.home, name='home'),
    path('createstate', views.createState, name='createstate'),
    path('statecommittee', views.stateCommittee, name='statecommittee'),
    path('volunteer', views.volunteer, name='volunteer'),
    path('alerts', views.alerts, name='alerts'),
    path('needs', views.needs, name='needs')
]