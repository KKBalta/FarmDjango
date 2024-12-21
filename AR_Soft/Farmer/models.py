from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.core.validators import EmailValidator

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="farmers")
    position = models.CharField(max_length=100)  # Farmer's position
    email = models.EmailField(null=True, blank=True, validators=[EmailValidator()])
    phone = PhoneNumberField(null=False, blank=False, default='+90000000000', region="TR")

    def __str__(self):
        return self.name

    def calculate_age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
