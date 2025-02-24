from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    #other fields as needed.