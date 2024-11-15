# farmers/models.py
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="farmers")
    position = models.CharField(max_length=100)  # Farmer's position in the company (e.g., 'Manager', 'Laborer', etc.)
    email = models.EmailField(null=True, blank=True)  # Optional field for the farmer's email

    def __str__(self):
        return self.name
