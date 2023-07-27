from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StateForm
from .models import StateCommittee, Volunteer, EndUser, State, Needs




# Create your views here.

""" ----VIEWS---- """

def home(request):

    endUsers = EndUser.objects.all()

    context = {'endUsers' : endUsers,}

    return render(request, 'base/user/viewuser.html', context)


def stateCommittee(request):

    stateCommittee = StateCommittee.objects.all()

    context = {'states' :stateCommittee,}
    

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

    #SET STATES

    states = State.objects.all()

    context = {'states': states}



    if request.method =='POST':

        username = request.POST.get('name')
        phone = request.POST.get('number')
        location = request.POST.get('location')
        stateid = request.POST.get('state')
        password = request.POST.get('password')
        email = request.POST.get('email')
        state = State.objects.get(id=stateid)

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

    return render(request, 'base/user/adduser.html', context)

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

        elif User.objects.filter(username=username):
            messages.info(request, 'Username Taken')
            return redirect('add-state')
        else:
             user = User.objects.create_user(username=username, email=email, password=password)
             user.save()

             StateCommittee.objects.create(host=user,name=username,phone=phone, state=state, location=location)

             return redirect('statecommittee') 
      

# --- EDIT EXISTING STATE ---


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
        user.username = username
        user.set_password(request.POST.get('password'))

        stateCommittee.save()
        user.save()

        return redirect('statecommittee')

    context = {'user': user, 'stateCommittee': stateCommittee, 'states': states}

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
       
       stateid = request.POST.get('state')
       

       username = request.POST.get('name')
       phone = request.POST.get('number')
       state = State.objects.get(id=stateid)
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

""" def loginPage(request):
    
   if request.user.is_authenticated : 
       return redirect('volunteer-home')
   

   if request.method == 'POST':
      username= request.POST.get('username')
      password = request.POST.get('password')
      print('pass', password)
     

      try: 
        user = User.objects.get(username=username)
        print('i user', user)

      except:
          messages.error(request, 'User not found')

      user_login = authenticate(request, username=username, password=password)
      print('a user', user_login)

      if user_login is not None:
          login(request, user_login)
          return redirect('volunteer-home')
      else : 
          messages.error(request,"username or password doesn't exist")

          return redirect('login')



   return render (request, 'Front/Login.html') """


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('volunteer-home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')
        
        
        user_login = authenticate(request, username=username, password=password)

        if user_login is not None:
            login(request, user_login)
            return redirect('volunteer-home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'Front/Login.html')

#Register Page

def register(request):
    states = State.objects.all()
    context = {'states': states}

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

       print('latitude', latitude)
       print('longitude', longitude)

       if User.objects.filter(email=email).exists():
           messages.info(request, 'Email already taken')
           return redirect('register')
       elif User.objects.filter(username=username):
           messages.info(request, 'username already taken')
           return redirect('register')
       else:
           user = User.objects.create_user(username=username, email=email, password=password)
           user.save()
           Volunteer.objects.create(host=user, name=username, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude)
           login(request, user)

           return redirect('volunteer-home')

    




    return render(request, 'Front/register.html', context)



def userRegister(request):

     states = State.objects.all()
     context = {'states': states}

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

       print('latitude', latitude)
       print('longitude', longitude)

       if User.objects.filter(email=email).exists():
           messages.info(request, 'Email already taken')
           return redirect('user-register')
       elif User.objects.filter(username=username):
           messages.info(request, 'username already taken')
           return redirect('user-register')
       else:
           user = User.objects.create_user(username=username, email=email, password=password)
           user.save()
           EndUser.objects.create(host=user, name=username, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude)
           login(request, user)

           return redirect('user-home')


     return render(request, 'Front/User/userRegister.html',context)


# Logout user

@login_required(login_url='login')
def logoutUser(request):
    logout(request)

    return redirect('login')


# VOLUNTEER HOME PAGE

@login_required(login_url='login')
def volunteerHome(request):

    if request.method == 'POST':
        
        requirements = request.POST.get('requirements')
        host = Volunteer.objects.filter(host=request.user)

        Needs.objects.create(host=host, requirements=requirements)

        return redirect('volunteer-home')

    return render(request, 'Front/volunteer.html')


# User home page

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


    
    
        
   
    

   


    
