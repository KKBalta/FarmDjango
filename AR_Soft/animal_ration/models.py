from django.db import models
from django.utils.timezone import now

class AnimalRationLog(models.Model):
    animal = models.ForeignKey(
        'Animal.Animal',  # Use string reference to the Animal model
        on_delete=models.CASCADE,
        related_name="ration_logs"
    )
    ration_table = models.ForeignKey(
        'ration_components.RationTable',  # Use string reference to the RationTable model
        on_delete=models.CASCADE,
        related_name="animal_logs"
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Whether this ration is currently active for the animal

    def __str__(self):
        return f"{self.animal.eartag} on {self.ration_table.name}"

    def save(self, *args, **kwargs):
        # Explicitly set start_date if it's None
        if not self.start_date:
            self.start_date = now()

        if self.is_active:
            # Debug the query
            last_active_log = AnimalRationLog.objects.filter(
                animal=self.animal,
                is_active=True
            ).order_by('-start_date').first()

            if last_active_log:
                print(f"Last active log: {last_active_log}")
                # Use self.start_date to set end_date for the last log
                last_active_log.end_date = self.start_date
                print(f"start date: {self.start_date}")
                last_active_log.is_active = False
                last_active_log.save()
            else:
                print(f"No active logs found for animal {self.animal.id}")

        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        """
        Handle deletion of the current log.
        Activate the most recent inactive log for the animal.
        """
        if self.is_active:
            # Find the most recent inactive log for the same animal
            previous_log = AnimalRationLog.objects.filter(
                animal=self.animal,
                is_active=False
            ).order_by('-start_date').first()

            if previous_log:
                # Activate the previous log and reset its end_date
                previous_log.is_active = True
                previous_log.end_date = None
                previous_log.save()

        super().delete(*args, **kwargs)