from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    user_type = models.IntegerField(null=True) # 0: Admin || 1:state committee || 2: Volunteer  || 3: user

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class State(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name


class StateCommittee(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField( null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, null=True)
    location = models.TextField(null=True) 
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)



    def __str__(self) -> str:
        return self.name


class Volunteer(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField(null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, null=True)
    location = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name
        


class EndUser(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField(null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    location = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name


class Alert(models.Model):
    host = models.ForeignKey(EndUser , on_delete=models.CASCADE,null=True)
    state_committee = models.ForeignKey(StateCommittee, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=200, null=True)
    status = models.IntegerField(default=0) # 0: pending || 1: open || 2: closed  
    is_verified_by_state = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    is_verified_by_admin = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    rejected_by = models.IntegerField(null=True, blank=True) #  0:admin || 1:state || 2:volunteer
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self) -> str:
        return self.content




class Needs(models.Model):
    host = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    state_committee = models.ForeignKey(StateCommittee, on_delete=models.CASCADE, null=True)
    requirements = models.TextField(null=True)
    status = models.IntegerField(default=0)  # 0:pending || 1:open || 2:closed
    is_verified_by_state = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    is_verified_by_admin = models.IntegerField(default=0) # 0:pending || 1:approved || 2:rejected
    rejected_by = models.IntegerField(null=True, blank=True) #  0:admin || 1:state || 2:volunteer
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =['-updated', '-created']

    def __str__(self) -> str:
        return self.requirements
    



class Product(models.Model):
    #host =
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    #category =
    # subcategory =  
    price = models.IntegerField(null=True) 

    def __str__(self) -> str:
        return self.title


class CartItem(models.Model):
    host = models.ForeignKey(EndUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.host.name
    
class Cart(models.Model):
    host = models.ForeignKey(EndUser, on_delete=models.CASCADE, null=True)
    products= models.ManyToManyField(CartItem, related_name='products', blank=True)
    active = models.IntegerField(default=0) # 0: active 1 : inactive

    def __str__(self) -> str:
        return self.host.name


class Order(models.Model):
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0) # 0: Pending 1: Approved 2: Rejected
   
    class Meta:
     ordering = ['-created']
