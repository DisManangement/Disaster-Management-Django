from django.shortcuts import render, redirect
from .models import State

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





def createState(request):

    if request.method == 'POST':

        State.objects.create(
            state_name= request.POST.get('name'),
            address = request.POST.get('address'),
            contact_number = request.POST.get('contact'),
            login_id= 3
        )

  
  
    return redirect('home')
    
    
        
   
    

   


    
