from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import StateForm
from .models import State, Volunteer, EndUser



# Create your views here.

""" ----VIEWS---- """

def home(request):

    endUsers = EndUser.objects.all()

    context = {'endUsers' : endUsers,}

    return render(request, 'base/user/viewuser.html', context)


def stateCommittee(request):

    states = State.objects.all()

    context = {'states' :states,}
    

    return render(request, 'base/stateCommittee/viewStateCommittee.html', context)

def volunteer(request):

    volunteers = Volunteer.objects.all()

    context ={'volunteers':volunteers}


    return render(request, 'base/volunteer/viewVolunteer.html', context)

def alerts(request):

    return render(request, 'base/alerts/alerts.html')

def needs(request):

    return render(request, 'base/needs/needs.html')

def addUser(request):

    if request.method =='POST':
        username = request.POST.get('name')
        phone = request.POST.get('number')
        location = request.POST.get('location')
        state = request.POST.get('state')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Already Taken')
            return redirect('add-user')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Already Exists')
            return redirect('add-user')
        else:
           user = User.objects.create(username=username, email=email, password=password)
           user.save()

           EndUser.objects.create(host=user, name=username, location=location, state=state, phone=phone)

           return redirect('/')

    return render(request, 'base/user/adduser.html')

def addState(request):

    return render(request, 'base/stateCommittee/addState.html')


def addVolunteer(request):

    return render(request, 'base/volunteer/addVolunteer.html')



"""---------- STATE CRUD OPERATIONS -----------"""

"""--- CREATE NEW STATE --- """

def createState(request):

    if request.method == 'POST':

        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('number')
        state = request.POST.get('state')
        location = request.POST.get('location')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('add-state')

        elif User.objects.filter(username=username):
            messages.info(request, 'Username Taken')
            return redirect('add-state')
        else:
             user = User.objects.create_user(username=username, email=email, password=password)
             user.save()

             State.objects.create(host=user,name=username,phone=phone, state=state, location=location)

             return redirect('statecommittee') 
      

""" --- EDIT EXISTING STATE --- """


def editState(request,pk):
    state = State.objects.get(id=pk)
    user = state.host

    print('user',user)
    
    form = StateForm(instance=state)


    if request.method == 'POST':
       
        email = request.POST.get('email')
        username = request.POST.get('name')
        tempUser = User.objects.filter(email=email)
        tempEmail = tempUser.username
        print('temp email', tempEmail)
        
        if User.objects.filter(email=email).exists():
            
            print('temp',tempUser)
            if user.email != User.objects.filter(email=email) :

             messages.info(request, 'Email Already Taken')
             return redirect(f'/editstate/{pk}')
            
        elif  User.objects.filter(username=username).exists():
            if user != User.objects.filter(username=username) :
                messages.info(request, 'Username Already Taken')
        
        else:
                  state.name= request.POST.get('name')
                  state.phone = request.POST.get('number')
                  state.state = request.POST.get('state')
                  state.location = request.POST.get('location')

                  user.email = email
                  user.username = username
                  user.password= request.POST.get('password')
        
                  state.save()
                  user.save()
        
                  return redirect('statecommittee')

    context ={'user':user, 'state':state}

    return render(request, 'base/stateCommittee/editState.html', context)

        
          

""" --- DELETE EXISTING STATE --- """

def deleteState(request):
    pass
        



""" <----------  STATE ENDS -------> """

  

""" ---------- VOLUNTEER CRUD OPERATIONS ------ """


def createVolunteer(request):
   if request.method == 'POST':
       username = request.POST.get('name')
       phone = request.POST.get('number')
       state = request.POST.get('state')
       location = request.POST.get('location')
       email = request.POST.get('email')
       password = request.POST.get('password')

       if User.objects.filter(email=email).exists():
           messages.info(request, 'Email already taken')
           return redirect('add-volunteer')
       elif User.objects.filter(username=username):
           messages.info(request, 'username already taken')
           return redirect('add-volunteer')
       else:
           user = User.objects.create(username=username, email=email, password=password)
           user.save()
           Volunteer.objects.create(host=user, name=username, phone=phone, state=state, location=location)

           return redirect('volunteer')
           

   
   
   


  
    
    
    
        
   
    

   


    
