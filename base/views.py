from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StateForm
from .models import StateCommittee, Volunteer, EndUser, State, Needs, User


# decorotors




# @login_required(login_url='login')
def userOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 3:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view



# @login_required(login_url='login')
def volunteerOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 2:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view



# @login_required(login_url='login')
def stateCommitteeOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 1:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view


# @login_required(login_url='login')
def adminOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view

def adminStateOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0 or request.user.user_type == 1 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view

# Create your views here.

""" ----VIEWS FOR ADMIN---- """

@login_required(login_url='login')
@adminStateOnly
def home(request):

    endUsers = EndUser.objects.all()

    context = {'endUsers' : endUsers,}

    return render(request, 'base/user/viewuser.html', context)


@login_required(login_url='login')
@adminOnly
def stateCommittee(request):

    stateCommittee = StateCommittee.objects.all()

    context = {'states' :stateCommittee,}
    

    return render(request, 'base/stateCommittee/viewStateCommittee.html', context)

@login_required(login_url='login')
@adminStateOnly
def volunteer(request):

    volunteers = Volunteer.objects.all()

    context ={'volunteers':volunteers}


    return render(request, 'base/volunteer/viewVolunteer.html', context)


@login_required(login_url='login')
@adminStateOnly
def alerts(request):

    return render(request, 'base/alerts/alerts.html')

def needs(request):

    return render(request, 'base/needs/needs.html')



def addState(request):

    #setting all states

    states = State.objects.all()
    context = {'states': states}

    return render(request, 'base/stateCommittee/addState.html', context)


def addVolunteer(request):

    #setting all states

    states = State.objects.all()
    context = {'states': states}

    return render(request, 'base/volunteer/addVolunteer.html', context)



"""---------- STATE CRUD OPERATIONS -----------"""

# --- CREATE NEW STATE ---

def createState(request):

    if request.method == 'POST':

        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('number')
        stateid = request.POST.get('state')
        location = request.POST.get('location')
        state = State.objects.get(id=stateid)
        
        
        print('id', stateid)
        print('state', state)
        

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('add-state')

       
        else:
             user = User.objects.create_user(name=username, email=email, password=password)
             user.save()

             StateCommittee.objects.create(host=user,name=username,phone=phone, state=state, location=location)

             return redirect('statecommittee') 
      

# --- EDIT EXISTING STATE ---


@login_required(login_url='login')
@adminOnly
def editState(request, pk):
    stateCommittee = StateCommittee.objects.select_related('host').get(id=pk)
    user = stateCommittee.host
    
    states = State.objects.exclude(id=stateCommittee.state.id)
    

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
        stateid = request.POST.get('state')
        state = State.objects.get(id=stateid)
        stateCommittee.name = request.POST.get('name')
        stateCommittee.phone = request.POST.get('number')
        stateCommittee.state = state
        stateCommittee.location = request.POST.get('location')

        user.email = email
        user.name = username
        user.set_password(request.POST.get('password'))

        stateCommittee.save()
        user.save()

        return redirect('statecommittee')

    context = {'user': user, 'stateCommittee': stateCommittee, 'states': states}

    return render(request, 'base/stateCommittee/editState.html', context)

# --- DELETE EXISTING STATE --- 
@login_required(login_url='login')
@adminOnly
def deleteState(request,pk):
    
    state = State.objects.get(id=pk)
    state.delete()
    return redirect('statecommittee')
    
        



#   ----------  STATE ENDS ------->

  

""" ---------- VOLUNTEER CRUD OPERATIONS ------ """

       

 # -----     DELETE EXISTING VOLUNTEER     -----

@login_required(login_url='login')
@adminOnly
def deleteVolunteer(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    volunteer.delete()

    return redirect('volunteer')



#  ----- EDIT VOLUNTEER  -----


def editVolunteer(request, pk):
    volunteer = Volunteer.objects.select_related('host').get(id=pk)
    user = volunteer.host

    states = State.objects.exclude(id=volunteer.state.id)



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
        stateid = request.POST.get('state')
        volunteer.name = request.POST.get('name')
        volunteer.phone = request.POST.get('number')
        volunteer.state = State.objects.get(id=stateid)
        volunteer.location = request.POST.get('location')

        user.email = email
        user.username = username
        user.set_password(request.POST.get('password'))

        volunteer.save()
        user.save()

        return redirect('volunteer')

    context = {'user': user, 'volunteer': volunteer, 'states':states}

    return render(request, 'base/volunteer/editVolunteer.html', context)
           

   
   
   
"""  ----  END USER CRUD OPERATIONS    ----- """

# ----    DELETE EXISTING USER    ---- 


def deleteUser(request, pk):
    user = EndUser.objects.get(id=pk)
    user.delete()
    return redirect('/')


# edit Enduser  

def editEndUser(request, pk):
    enduser = EndUser.objects.select_related('host').get(id=pk)
    user = enduser.host
    states = State.objects.exclude(id=enduser.state.id)

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
        

        stateid = request.POST.get('state')
        # Update state and user data
        enduser.name = request.POST.get('name')
        enduser.phone = request.POST.get('number')
        enduser.state = State.objects.get(id=stateid)
        enduser.location = request.POST.get('location')

        user.email = email
        user.username = username
        user.set_password(request.POST.get('password'))

        enduser.save()
        user.save()

        return redirect('/')

    context = {'user': user, 'enduser': enduser, 'states':states}

    return render(request, 'base/user/editEndUser.html', context)





""" ------     HOME PAGES     ------ """

#Login Page




def loginPage(request):
    if request.user.is_authenticated:
         if request.user.user_type == 3:
           return redirect('user-home')
         elif request.user.user_type == 2:
             return redirect('volunteer-home')
         else:
             return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')
        
        
        user_login = authenticate(request, email=email, password=password)

        if user_login is not None:
            login(request, user_login)
            if user_login.user_type == 3:
                return redirect('user-home')
            elif user_login.user_type == 2:
                return redirect('volunteer-home')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
 
    return render(request, 'Front/Login.html')

#Register Pages

# State Register Page

def stateRegister(request):

    states = State.objects.all()
    context = {'states': states}

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        stateid = request.POST.get('state')
        name = request.POST.get('name')    
        phone = request.POST.get('number')
        state = State.objects.get(id=stateid)
        location = request.POST.get('location')
        email = request.POST.get('email')
        password = request.POST.get('password')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        usertype =request.POST.get('usertype')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Already Taken')
            return redirect('state-register')
        elif User.objects.filter(username=name).exists():
            messages.info(request, 'Username Already Taken')
            return redirect('state-register')
        
        else:
            user = User.objects.create_user(username=name, name=name, user_type=usertype, email=email, password=password)
           
            state_committee = StateCommittee.objects.create(host=user, name=name, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude)
             
            user.save()
            state_committee.save()
            login(request, user)

            return redirect('home')
        



    return render(request, 'base/stateCommittee/stateRegister.html', context)

#VOLUNTEER REGISTER PAGE

def register(request):
    states = State.objects.all()
    context = {'states': states}

    if request.user.is_authenticated:
        return render('volunteer-home')

    if request.method == 'POST':
       
       stateid = request.POST.get('state')
       

       username = request.POST.get('name')
       phone = request.POST.get('number')
       state = State.objects.get(id=stateid)
       location = request.POST.get('location')
       email = request.POST.get('email')
       password = request.POST.get('password')
       latitude = request.POST.get('latitude')
       longitude = request.POST.get('longitude')
       usertype = request.POST.get('usertype')

       print('latitude', latitude)
       print('longitude', longitude)

       if User.objects.filter(email=email).exists():
           messages.info(request, 'Email already taken')
           return redirect('register')
       if User.objects.filter(username=username).exists():
           messages.info(request, 'username already Taken')
           return redirect('register')
      
       else:
           user = User.objects.create_user(name=username,username=username, email=email,user_type=usertype, password =password)
           user.save()
           Volunteer.objects.create(host=user, name=username, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude)
           login(request, user)

           return redirect('volunteer-home')

    




    return render(request, 'Front/register.html', context)


#User Register Page


def userRegister(request):

     states = State.objects.all()
     context = {'states': states}

     if request.user.is_authenticated:
         return redirect('user-home')

     if request.method == 'POST':
       
       stateid = request.POST.get('state')
       

       username = request.POST.get('name')
       phone = request.POST.get('number')
       state = State.objects.get(id=stateid)
       location = request.POST.get('location')
       email = request.POST.get('email')
       password = request.POST.get('password')
       latitude = request.POST.get('latitude')
       longitude = request.POST.get('longitude')
       user_type = request.POST.get('usertype')

       print('latitude', latitude)
       print('longitude', longitude)

       if User.objects.filter(email=email).exists():
           messages.info(request, 'Email already taken')
           return redirect('user-register')
       elif User.objects.filter(username=username).exists():
           messages.info(request, 'username already taken')
           return redirect('user-register')
       else:
           user = User.objects.create_user(username=username,name=username,user_type=user_type, email=email, password=password)
           user.save()
           EndUser.objects.create(host=user, name=username, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude)
           login(request, user)

           return redirect('user-home')


     return render(request, 'Front/User/userRegister.html',context)


# Logout user


def logoutUser(request):
    logout(request)

    return redirect('login')


# VOLUNTEER HOME PAGE

@login_required(login_url='login')
@volunteerOnly
def volunteerHome(request):

    pendingNeeds = Needs.objects.filter(status=0)

    activeNeeds = Needs.objects.filter(status=1)

    closedNeeds = Needs.objects.filter(status=2)

    volunteer_state = Volunteer.objects.get(host=request.user).state

    context = {'pendingNeeds':pendingNeeds, 'activeNeeds': activeNeeds, 'closedNeeds':closedNeeds, 'volunteer_state':volunteer_state}

    if request.method == 'POST':
        
        requirements = request.POST.get('requirements')
        volunteer = Volunteer.objects.get(host=request.user)

        Needs.objects.create(host=volunteer, requirements=requirements)

        return redirect('volunteer-home')

    return render(request, 'Front/volunteer.html', context)


# User home page
@login_required(login_url='login')
@userOnly 
def userHome(request):
    return render(request, 'Front/user/userhome.html')



#  CREATE ALERTS




# CHANGE STATUS OF ALERT (UPDATE)

def updateAlert(request):
    pass

# CREATE NEEDS

def alert(request):
    pass


# CHANGE STATUS OF NEEDS (UPDATE)

def updateNeeds(request):
    pass


    
    
        
   
    

   


    
