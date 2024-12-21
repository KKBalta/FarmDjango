# animal_ration/models.py
from django.db import models
from Animal.models import Animal
from ration_components.models import RationTable

class AnimalRationLog(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="ration_logs")
    ration_table = models.ForeignKey(RationTable, on_delete=models.CASCADE, related_name="animal_logs")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Whether this ration is currently active for the animal

    def __str__(self):
        return f"{self.animal.eartag} on {self.ration_table.name}"

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate other logs for the same animal if this is active
            AnimalRationLog.objects.filter(animal=self.animal, is_active=True).update(is_active=False, end_date=self.start_date)
        super().save(*args, **kwargs)
