from django.shortcuts import render, redirect
from .models import State
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import StateForm


# Create your views here.



def home(request):

    return render(request, 'base/user/viewuser.html')


def stateCommittee(request):
    

    return render(request, 'base/stateCommittee/viewStateCommittee.html')

def volunteer(request):


    return render(request, 'base/volunteer/viewVolunteer.html')

def alerts(request):

    return render(request, 'base/alerts/alerts.html')

def needs(request):

    return render(request, 'base/needs/needs.html')

def addUser(request):

    return render(request, 'base/user/adduser.html')

def addState(request):

    return render(request, 'base/stateCommittee/addState.html')


def addVolunteer(request):

    return render(request, 'base/volunteer/addVolunteer.html')





def createState(request):

    if request.method == 'POST':

        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('number')
        state = request.POST.get('state')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('add-state')

        elif User.objects.filter(username=username):
            messages.info(request, 'Username Taken')
            return redirect('add-state')
        else:
             user = User.objects.create_user(username=username, email=email, password=password)
             user.save()

             State.objects.create(host=user,name=username,phone=phone, state=state)

             return redirect('statecommittee') 
      


def editState(request):
    pass
        

  
  
    
    
    
        
   
    

   


    
