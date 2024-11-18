# weight/models.py
from django.db import models
from Animal.models import Animal

class Weight(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="weights")
    weight = models.FloatField()  # The weight of the animal (e.g., in kg or pounds)
    recorded_at = models.DateField(auto_now_add=True)  # Automatically set the date when the record is created

    class Meta:
        # Enforce unique weight records per animal per month
        constraints = [
            models.UniqueConstraint(
                fields=['animal', 'recorded_at'], name='unique_weight_per_month'
            )
        ]

    def __str__(self):
        return f"{self.animal.eartag} - {self.weight} kg on {self.recorded_at}"
