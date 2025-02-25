from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    