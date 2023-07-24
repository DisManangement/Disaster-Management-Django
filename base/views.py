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

# --- CREATE NEW STATE ---

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
      

# --- EDIT EXISTING STATE ---


def editState(request, pk):
    state = State.objects.select_related('host').get(id=pk)
    user = state.host

    print('user', user)

    form = StateForm(instance=state)

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')

        # Check if the given email is already taken by another user
        existing_user = User.objects.filter(email=email).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Email Already Taken')
            return redirect(f'/editstate/{pk}')

        # Check if the given username is already taken by another user
        existing_user = User.objects.filter(username=username).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Username Already Taken')
            return redirect(f'/editstate/{pk}')

        # Update state and user data
        state.name = request.POST.get('name')
        state.phone = request.POST.get('number')
        state.state = request.POST.get('state')
        state.location = request.POST.get('location')

        user.email = email
        user.username = username
        user.set_password(request.POST.get('password'))

        state.save()
        user.save()

        return redirect('statecommittee')

    context = {'user': user, 'state': state}

    return render(request, 'base/stateCommittee/editState.html', context)

# --- DELETE EXISTING STATE --- 

def deleteState(request,pk):
    
    state = State.objects.get(id=pk)
    state.delete()
    return redirect('statecommittee')
    
        



#   ----------  STATE ENDS ------->

  

""" ---------- VOLUNTEER CRUD OPERATIONS ------ """

#  -----     CREATE VOLUNTEER      ------


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
       

 # -----     DELETE EXISTING VOLUNTEER     -----

def deleteVolunteer(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    volunteer.delete()

    return redirect('volunteer')



#  ----- EDIT VOLUNTEER  -----


def editVolunteer(request, pk):
    volunteer = Volunteer.objects.select_related('host').get(id=pk)
    user = volunteer.host

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')

        # Check if the given email is already taken by another user
        existing_user = User.objects.filter(email=email).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Email Already Taken')
            return redirect(f'/editvolunteer/{pk}')

        # Check if the given username is already taken by another user
        existing_user = User.objects.filter(username=username).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Username Already Taken')
            return redirect(f'/editvolunteer/{pk}')

        # Update state and user data
        volunteer.name = request.POST.get('name')
        volunteer.phone = request.POST.get('number')
        volunteer.state = request.POST.get('state')
        volunteer.location = request.POST.get('location')

        user.email = email
        user.username = username
        user.set_password(request.POST.get('password'))

        volunteer.save()
        user.save()

        return redirect('volunteer')

    context = {'user': user, 'volunteer': volunteer}

    return render(request, 'base/volunteer/editVolunteer.html', context)
           

   
   
   
"""  ----  END USER CRUD OPERATIONS    ----- """

# ----    DELETE EXISTING USER    ---- 


def deleteUser(request, pk):
    user = EndUser.objects.get(id=pk)
    user.delete()
    return redirect('/')



def editEndUser(request, pk):
    enduser = EndUser.objects.select_related('host').get(id=pk)
    user = enduser.host

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')

        # Check if the given email is already taken by another user
        existing_user = User.objects.filter(email=email).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Email Already Taken')
            return redirect(f'/edituser/{pk}')

        # Check if the given username is already taken by another user
        existing_user = User.objects.filter(username=username).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Username Already Taken')
            return redirect(f'/edituser/{pk}')

        # Update state and user data
        enduser.name = request.POST.get('name')
        enduser.phone = request.POST.get('number')
        enduser.state = request.POST.get('state')
        enduser.location = request.POST.get('location')

        user.email = email
        user.username = username
        user.set_password(request.POST.get('password'))

        enduser.save()
        user.save()

        return redirect('/')

    context = {'user': user, 'enduser': enduser}

    return render(request, 'base/user/editEndUser.html', context)




  
    
    
    
        
   
    

   


    
