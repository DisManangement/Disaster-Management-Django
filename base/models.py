from typing import Any
from django.db import models
from django.contrib.auth.models import User


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
    latitiude = models.TextField(null=True)
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
    remark = models.CharField(max_length=200, null=True)
    status = models.IntegerField(default=0) # 0: pending || 1: closed  


class Needs(models.Model):
    host = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    requirements = models.TextField(null=True)
    status = models.IntegerField(default=0)  # 0:pending || 1:open || 2:closed
    is_verified_by_state = models.IntegerField(default=0)
    is_verified_by_admin = models.IntegerField(default=0)
   




    

