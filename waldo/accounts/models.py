
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    date_first_hired = models.DateField(null=True, blank=True, verbose_name="Date of first hired")
    is_admin = models.BooleanField(default=False, verbose_name="Administrator status")

    def __str__(self):
        return self.username