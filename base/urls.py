from django.urls import path
from . import views


urlpatterns= [
    path('', views.home, name='home'),
    path('createstate', views.createState, name='createstate'),
    path('statecommittee', views.stateCommittee, name='statecommittee'),
    path('volunteer', views.volunteer, name='volunteer'),
    path('alerts', views.alerts, name='alerts'),
    path('needs', views.needs, name='needs'),
    
    path('addstate', views.addState, name='add-state'),
    path('addvolunteer', views.addVolunteer, name='add-volunteer'),
    path('createstate', views.createState, name='create-state'),
    path('editstate/<str:pk>', views.editState, name='edit-state'),
    path('editvolunteer/<str:pk>', views.editVolunteer, name='edit-volunteer'),
    path('edituser/<str:pk>', views.editEndUser, name='edit-user'),
   
    path('deletestate/<str:pk>', views.deleteState, name='delete-state'),
    path('deleteuser/<str:pk>', views.deleteUser, name='delete-user'),
    path('deletevolunteer/<str:pk>', views.deleteVolunteer, name='delete-volunteer'),
    path('volunteerhome', views.volunteerHome, name='volunteer-home'),
    path('userhome', views.userHome, name='user-home-temp'),
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('userregister', views.userRegister, name='user-register'),
    path('stateregister', views.stateRegister, name='state-register'),
    path('logout', views.logoutUser, name='logout'),

    path('needsverifybystate/<str:pk>', views.needsVerifyByState, name='needs-verify-by-state'),
    path('needsrejectbystate/<str:pk>', views.needsRejectByState, name='needs-reject-by-state'),

    path('closeneeds/<str:pk>', views.closeNeeds, name='close-needs'),
    path('deleteneeds/<str:pk>', views.deleteNeeds, name='delete-needs'),

    path('user/request/alert', views.userRequestPage, name='user-home'),

    path('approvealert/<str:pk>', views.verifyAlert, name='approve-alert'),
    path('rejectalert/<str:pk>', views.rejectAlert, name='reject-alert'),

    path('deletealert/<str:pk>', views.deleteAlert, name='delete-alert'),
    path('closealert/<str:pk>', views.closeAlert, name='close-alert')

]