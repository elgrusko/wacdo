from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}"
