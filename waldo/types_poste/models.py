from django.db import models


class TypePoste(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        # Normalize label by stripping whitespace and converting to title case
        self.label = self.label.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label
