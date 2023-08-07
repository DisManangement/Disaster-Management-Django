from django.shortcuts import render, redirect
import os
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StateForm
from .models import StateCommittee, Volunteer, EndUser, State, Needs, User, Alert, Product, Cart, CartItem, Order


# decorotors





def userOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 3:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view




def volunteerOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 2:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view




def stateCommitteeOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 1:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view



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

def endUserOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 3 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view

def adminStateVolunteerOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0 or request.user.user_type == 1 or request.user.user_type == 2 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view

def adminStateUserOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0 or request.user.user_type == 1 or request.user.user_type == 3 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view



# Create your views here.

""" ----VIEWS FOR ADMIN---- """

@login_required(login_url='login')
@adminStateOnly
def home(request):

    
    if request.user.user_type == 0:
       endUsers = EndUser.objects.all()
    if request.user.user_type == 1:
        state_committee = StateCommittee.objects.get(host=request.user)
        state = state_committee.state

        endUsers = EndUser.objects.filter(state=state)
  
        
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
    if request.user.user_type == 0 :

     volunteers = Volunteer.objects.all()
    
    if request.user.user_type == 1 :

        state_committee = StateCommittee.objects.get(host=request.user)
        state = state_committee.state 

        volunteers = Volunteer.objects.filter(state=state)

    context ={'volunteers':volunteers}


    return render(request, 'base/volunteer/viewVolunteer.html', context)


@login_required(login_url='login')
@adminStateOnly
def alerts(request):
    if request.user.user_type == 0 :
         pendingAlerts = Alert.objects.filter(is_verified_by_state=1, status=0)
         openAlerts = Alert.objects.filter(status=1)
         closedAlerts = Alert.objects.filter(status=2)
    if request.user.user_type == 1:
        stateCommittee = StateCommittee.objects.get(host=request.user)

        pendingAlerts = Alert.objects.filter(state_committee=stateCommittee, status=0, is_verified_by_state=0)
        openAlerts = Alert.objects.filter(state_committee=stateCommittee, status=1)
        closedAlerts = Alert.objects.filter(state_committee=stateCommittee, status=2)

    context = {
            'pendingAlerts':pendingAlerts,
            'openAlerts' : openAlerts,
            'closedAlerts' : closedAlerts
    }
    

    return render(request, 'base/alerts/alerts.html', context)


@login_required(login_url='login')
@adminStateOnly
def needs(request):

    if request.user.user_type == 0 :
        needs = Needs.objects.filter(is_verified_by_state=1, status=0)
        open_needs = Needs.objects.filter(status=1)
        closed_needs = Needs.objects.filter(status=2)
    if request.user.user_type == 1 :
        state_committee = StateCommittee.objects.get(host=request.user)
        needs = Needs.objects.filter(state_committee=state_committee, status=0, is_verified_by_state=0)
        open_needs = Needs.objects.filter(status=1, state_committee=state_committee)
        closed_needs = Needs.objects.filter(status=2, state_committee=state_committee)


    context = {
        'needs' : needs,
        'open_needs':open_needs,
        'closed_needs' : closed_needs
               
               }

    return render(request, 'base/needs/needs.html', context)



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
             user = User.objects.create_user(name=username,username=username, email=email, password=password)
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
@adminStateOnly
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
@login_required(login_url='login')
@adminStateOnly
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

login_required(login_url='login')
def logoutUser(request):
    logout(request)

    return redirect('login')


# VOLUNTEER HOME PAGE

@login_required(login_url='login')
@volunteerOnly
def volunteerHome(request):
    
    volunteer = Volunteer.objects.get(host=request.user)
    
    pendingNeeds = Needs.objects.filter(host=volunteer,status=0)

    activeNeeds = Needs.objects.filter(host=volunteer,status=1)

    closedNeeds = Needs.objects.filter(host=volunteer,status=2)

    volunteer_state = Volunteer.objects.get(host=request.user).state

    page = 'volunteer'

    context = {'pendingNeeds':pendingNeeds, 'activeNeeds': activeNeeds, 'closedNeeds':closedNeeds, 'volunteer_state':volunteer_state, 'page':page}

    if request.method == 'POST':
        
        requirements = request.POST.get('requirements')
        volunteer = Volunteer.objects.get(host=request.user)
        state = volunteer.state

        print(state)
        
        state_committee = StateCommittee.objects.filter(state=state).first()

        print(state_committee)

        Needs.objects.create(host=volunteer,state_committee=state_committee, requirements=requirements)

        return redirect('volunteer-home')

    return render(request, 'Front/volunteer.html', context)


# User home page
@login_required(login_url='login')
@userOnly 
def userHome(request):
    return render(request, 'Front/user/userhome.html')







# CHANGE STATUS OF NEEDS (UPDATE)

# VERIFY BY STATE
@login_required(login_url='login')
@adminStateOnly
def needsVerifyByState(request, pk):

    need = Needs.objects.get(id=pk)

    if request.user.user_type == 1:

       need.is_verified_by_state = 1
    
    if request.user.user_type == 0 :

        need.is_verified_by_admin = 1
        need.status = 1

    need.save()

    return redirect ('needs')

# REJECT BY STATE
@login_required(login_url='login')
@adminStateOnly
def needsRejectByState(request, pk):
    
    need = Needs.objects.get(id=pk)

    if request.user.user_type == 1:

      need.is_verified_by_state = 2
      need.status = 2
      need.rejected_by = 1

    if request.user.user_type == 0:

        need.is_verified_by_admin =2
        need.status =2
        need.rejected_by = 0

    need.save()

    return redirect('needs')


# CLOSE NEEDS
@login_required(login_url='login')
@adminStateVolunteerOnly
def closeNeeds(request, pk):
    
    if request.user.user_type == 0 :
        need = Needs.objects.get(id=pk)

        need.status = 2
        need.rejected_by= 0

        need.save()

        return redirect('needs')

    elif request.user.user_type == 1 :

        need = Needs.objects.get(id=pk)
        need.status = 2
        need.rejected_by = 1
        need.save()

        return redirect('needs')

    elif request.user.user_type == 2 :

        need = Needs.objects.get(id=pk)
        need.status = 2
        need.rejected_by = 2
        need.save()

        return redirect('volunteer-home')
    
    else:
        return redirect('user-home')

    
    
@login_required(login_url='login')
@adminStateVolunteerOnly
def deleteNeeds(request,pk):
    need = Needs.objects.get(id=pk)
    need.delete()

    if request.user.user_type == 0 or request.user.user_type == 1:
        return redirect('needs')
    elif request.user.user_type ==2 :
        return redirect('volunteer-home')
    else:
        return redirect('user-home')
   
    
@login_required(login_url='login')
@userOnly
def userRequestPage(request):

    endUser = EndUser.objects.get(host=request.user)

    pendingAlerts = Alert.objects.filter(host=endUser,status=0)

    activeAlerts = Alert.objects.filter(host=endUser,status=1)

    closedAlerts = Alert.objects.filter(host=endUser,status=2)
    
    endUser_state = endUser.state

    context = {'pendingAlerts':pendingAlerts, 'activeAlerts':activeAlerts, 'closedAlerts':closedAlerts, 'endUser_state':endUser_state}



    if request.method == 'POST':
       
       content = request.POST.get('alertcontent') 
       endUser = EndUser.objects.get(host=request.user)
       state = endUser.state
       state_committee = StateCommittee.objects.filter(state=state).first()

       Alert.objects.create(host=endUser, content=content, state_committee=state_committee)

       return redirect('user-home')





    return render(request, 'Front/User/userRequest.html', context)



# Verify Alert


@login_required(login_url='login')
@adminStateOnly
def verifyAlert(request,pk):
    alert = Alert.objects.get(id=pk)

    if request.user.user_type == 1:

       alert.is_verified_by_state = 1
    
    if request.user.user_type == 0 :

        alert.is_verified_by_admin = 1
        alert.status = 1

    alert.save()

    return redirect ('alerts')



#Reject Alert

@login_required(login_url='login')
@adminStateOnly
def rejectAlert(request,pk):
    
    alert = Alert.objects.get(id=pk)

    if request.user.user_type == 1:

      alert.is_verified_by_state = 2
      alert.status = 2
      alert.rejected_by = 1

    if request.user.user_type == 0:

        alert.is_verified_by_admin =2
        alert.status =2
        alert.rejected_by = 0

    alert.save()

    return redirect('alerts')


# Delete Alert
@login_required(login_url='login')
@adminStateUserOnly
def deleteAlert(request, pk):
    alert = Alert.objects.get(id=pk)
    alert.delete()

    if request.user.user_type == 0 or request.user.user_type == 1:
        return redirect('alerts')
    elif request.user.user_type ==2 :
        return redirect('volunteer-home')
    else:
        return redirect('user-home')
    

@login_required(login_url='login')
@adminStateUserOnly
def closeAlert(request, pk):
    
    if request.user.user_type == 0 :
        alert = Alert.objects.get(id=pk)

        alert.status = 2
        alert.rejected_by= 0

        alert.save()

        return redirect('alerts')

    elif request.user.user_type == 1 :

        alert = Alert.objects.get(id=pk)
        alert.status = 2
        alert.rejected_by = 1
        alert.save()

        return redirect('alerts')

    elif request.user.user_type == 3 :

        alert = Alert.objects.get(id=pk)
        alert.status = 2
        alert.rejected_by = 2
        alert.save()

        return redirect('user-home')
    
    else:
        return redirect('volunteer-home')


def mapAlert(request,pk):
    user = User.objects.get(id=pk)
    volunteer = Volunteer.objects.get(host=user)
    volunteer_state = volunteer.state
    state_committee = StateCommittee.objects.filter(state=volunteer_state).first()
    alerts = Alert.objects.filter(state_committee=state_committee).first()

    context = {'alerts': alerts}

    return render(request, 'Front/mapAlert.html', context)



# PRODUCTS

def viewProducts(request):
  products = Product.objects.all()
  context = {'products': products}
  return render(request, 'base/products/viewProduct.html', context)

# ADD PRODUCTS

def addProduct(request):

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        Product.objects.create(title=title, description=description, price=price, image=image)

        return redirect('products')





    return render(request, 'base/products/addProduct.html')

# DELETE PRODUCTS

def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('products')


# EDIT PRODUCTS

def editProduct(request,pk):
    product = Product.objects.get(id=pk)
    context = {"product": product}

    if request.method == 'POST':
        product= Product.objects.get(id=pk)
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        if len(request.FILES) !=0:
            if len(product.image) > 0:
                os.remove(product.image.path)
            product.image = image
            
        product.title =title
        product.description = description
        product.price = price
        product.save()
        return redirect('products')


    return render(request, 'base/products/editProduct.html', context)


# view all products for users

def userProductView(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'Front/User/productView.html', context)


# adding items to the Cart

def addCart(request,pk):
    
    product = Product.objects.get(id=pk)
    host = EndUser.objects.get(host=request.user)

    cartItem = CartItem.objects.create(host=host, product=product)
    cartItem.save()
    cart = Cart.objects.get(host=host, active=0)
    cart.products.add(cartItem)


    return redirect('cart')


# cart for users

def cart(request):
    user = EndUser.objects.get(host=request.user)
    cart = Cart.objects.filter(host=user, active =0).first()
    print(cart)
    items = cart.products.all()

    total_price_list  = [x.product.price * x.quantity for x in list(items)]
    
    item_total = sum(total_price_list)
    tax = item_total * 0.10
    to_pay = item_total + tax
    

   

    context = {'cart': cart, 'items':items, 'item_total':item_total, 'tax': tax, 'to_pay': to_pay}
    return render(request, 'Front/User/cart.html', context)



# count increment for cart items

def countIncrement(request,pk):

    cartItem = CartItem.objects.get(id=pk)
    cartItem.quantity +=1
    cartItem.save()
    
    return redirect('cart')


# count decrement for cart items

def countDecrement(request,pk):
    cartItem = CartItem.objects.get(id=pk)


    if cartItem.quantity == 1 :
        cartItem.delete()
    else:
        cartItem.quantity -= 1
        cartItem.save()
    
    return redirect('cart')
    


# create order

def createOrder(request, pk):
    host = EndUser.objects.get(host=request.user)
    cart= Cart.objects.get(id=pk)
    Order.objects.create(cart= cart)
    cart.active = 1
    cart.save()
    Cart.objects.create(host=host)


    return redirect('cart')



# View Order

def viewOrder(request):

    orders = Order.objects.filter(status=0)

    context = {'orders':orders}

    return render(request, 'base/orders/orderView.html', context)

# Accept Order

def acceptOrder(request, pk):

    order = Order.objects.get(id=pk)
    order.status = 1  #order accepted
    order.save()

    return redirect('order-view')

# Reject Order

def rejectOrder(request, pk):

    order = Order.objects.get(id=pk)
    order.status = 2 # order rejected
    order.save()

    return redirect('order-view')

    