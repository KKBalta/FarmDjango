from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()  # Changed from 'age' to 'birth_date'
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="farmers")
    position = models.CharField(max_length=100)  # Farmer's position in the company (e.g., 'Manager', 'Laborer', etc.)
    email = models.EmailField(null=True, blank=True)  # Optional field for the farmer's email

    def __str__(self):
        return self.name

    def calculate_age(self):
        from datetime import date
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
