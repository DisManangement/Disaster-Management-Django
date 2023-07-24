from typing import Any
from django.db import models
from django.contrib.auth.models import User


class State(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField( null=True)
    state = models.CharField(max_length=200, null=True)
    location = models.TextField(null=True)
    latitiude = models.TextField(null=True)
    longitude = models.TextField(null=True)



    def __str__(self) -> str:
        return self.name







    

