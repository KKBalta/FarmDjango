from django.utils.timezone import localtime, make_aware, is_naive
from django.db import models
from Farmer.models import Company  # Import Company model from the company app
from animal_ration.models import AnimalRationLog
from ration_components.models import RationTableComponent

class Animal(models.Model):
    eartag = models.CharField(max_length=255, unique=True)  # Unique identifier for the animal
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="animals")  # Link to parent Company
    race = models.CharField(max_length=255, null=True)  # Breed of the animal
    gender = models.BooleanField(null=True)  # True for male, False for female
    room = models.CharField(max_length=255)  # Location or room where the animal resides
    cost = models.FloatField(null=True, blank=True)  # Cost of the animal
    is_slaughtered = models.BooleanField(default=False)  # Flag indicating if the animal went to slaughter
    feed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Cost of feeding the animal
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save

    def __str__(self):
        return f"{self.eartag} ({self.race})"

    
#### Animal Grouping ####


class Group(models.Model):
    name = models.CharField(max_length=255)  # Name of the group
    description = models.TextField(null=True, blank=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    dry_matter = models.FloatField(null=True, blank=True)  # Dry matter content of the group

    def __str__(self):
        return self.name


class AnimalGroup(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='animal_groups')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='animal_groups')
    assigned_at = models.DateTimeField(auto_now_add=True)  # When the animal was added to the group

    class Meta:
        unique_together = ('animal', 'group')  # Ensure an animal can't be assigned to the same group multiple times

    def __str__(self):
        return f"{self.animal.eartag} in {self.group.name}"
