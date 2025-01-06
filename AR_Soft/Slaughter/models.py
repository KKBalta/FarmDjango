from django.db import models
from Animal.models import Animal  # Import the Animal model
from django.utils import timezone

class Slaughter(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='slaughters')
    carcas_weight = models.FloatField(default=0.0, blank=False, null=False)
    sale_price = models.FloatField(default=0.0, blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)
    kdv = models.FloatField(default=0.0, blank=True)  # Default KDV to 0.0

    
    def save(self, *args, **kwargs):
        # Update the is_slaughter field in the Animal model
        if self.animal:
            self.animal.is_slaughtered = True
            self.animal.save(update_fields=['is_slaughtered'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal.eartag} - {self.carcas_weight}kg on {self.date}"
    
    def calculate_profit(self):
        # Ensure feed_cost and cost are not None
        animal_cost = self.animal.cost or 0.0
        feed_cost = float(self.animal.feed_cost or 0.0)
        total = (self.sale_price * self.carcas_weight)
        tax = total * (self.kdv)  # Calculate tax (KDV)
        
        # Profit calculation
        return total - (animal_cost + feed_cost + tax)
