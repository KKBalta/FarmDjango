# Slaughter/models.py
from django.db import models
from Animal.models import Animal

class Slaughter(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="slaughters")
    date = models.DateField()  # Date of slaughter
    carcas_weight = models.FloatField()  # Carcass weight in kilograms
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)  # Sale price of the animal
    kdv = models.BooleanField(default=False)  # Indicates whether the tax is applied

    def __str__(self):
        return f"{self.animal.eartag} - {self.carcas_weight}kg on {self.date}"
