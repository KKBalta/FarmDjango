# weight/models.py
from django.db import models
from Animal.models import Animal
from django.utils import timezone  # To get the current time

class Weight(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="weights")
    weight = models.FloatField()  # The weight of the animal in kilograms
    recorded_at = models.DateTimeField(default=timezone.now)  # Change to DateTimeField to store date and time

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['animal', 'recorded_at'], name='unique_weight_per_date')
        ]

    def __str__(self):
        return f"{self.animal.eartag} - {self.weight} kg on {self.recorded_at}"
