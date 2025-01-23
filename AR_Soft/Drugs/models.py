from django.db import models
from django.utils.timezone import now
from Animal.models import Animal

class Vaccine(models.Model):
    name = models.CharField(max_length=255)  # Name of the vaccine
    description = models.TextField(null=True, blank=True)  # Optional description of the vaccine
    manufacturer = models.CharField(max_length=255, null=True, blank=True)  # Manufacturer details
    created_at = models.DateTimeField(auto_now_add=True)  # When the vaccine entry was created

    def __str__(self):
        return self.name


class AnimalVaccineRecord(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="vaccine_records")  # Link to the animal
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="vaccine_records")  # Link to the vaccine
    date_administered = models.DateField(default=now)  # Date when the vaccine was administered
    administered_by = models.CharField(max_length=255, null=True, blank=True)  # Name of the person who administered it
    remarks = models.TextField(null=True, blank=True)  # Additional notes or remarks

    def __str__(self):
        return f"{self.animal.eartag} - {self.vaccine.name} ({self.date_administered})"
