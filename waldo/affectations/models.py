from django.db import models
from django.conf import settings
from restaurants.models import Restaurant
from types_poste.models import TypePoste


class Affectation(models.Model):
    collaborator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="affectations"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        related_name="affectations"
    )
    position_type = models.ForeignKey(
        TypePoste,
        on_delete=models.PROTECT,
        related_name="affectations"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        # by default, the affectations will be ordered by start_date descending (most recent first) when we query them
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.collaborator} -> {self.restaurant} ({self.position_type})"