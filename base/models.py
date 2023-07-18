from django.db import models
from django.contrib.auth.models import User



class Login(models.Model):
    username = models.EmailField(unique=True,)
    usertype =models.IntegerField()

    def __str__(self) -> str:
        return self.username

class State(models.Model):
    state_name = models.CharField(max_length=200)
    address = models.TextField(max_length=300)
    contact_number = models.BigIntegerField()
    login_id = models.IntegerField()


    def __str__(self) -> str:
        return self.state_name
