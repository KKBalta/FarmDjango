# animal/models.py
from django.db import models
from Farmer.models import Company  # Import Company model from the company app

class Animal(models.Model):
    eartag = models.CharField(max_length=255, unique=True)  # Unique identifier for the animal
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="animals")  # Link to parent Company
    race = models.CharField(max_length=255,null=True)  # Breed of the animal
    gender = models.BooleanField(null=True)  # True for male, False for female
    room = models.CharField(max_length=255)  # Location or room where the animal resides
    cost = models.FloatField(null=True, blank=True)  # Cost of the animal
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    feed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Cost of feeding the animal
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save


    def __str__(self):
        return f"{self.eartag} ({self.race})"
