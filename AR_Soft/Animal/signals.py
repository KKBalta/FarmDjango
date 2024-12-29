from django.db.models.signals import post_save
from django.utils.timezone import now
from django.dispatch import receiver
from animal_ration.models import AnimalRationLog
from ration_components.models import RationTable
from .models import Animal  # Import the Animal model

@receiver(post_save, sender=Animal)
def assign_default_ration(sender, instance, created, **kwargs):
    if created:  # Only run when a new animal is created
        default_ration_table = RationTable.objects.filter(name="Base Ration").first()

        if default_ration_table:
            # Assign the default ration
            AnimalRationLog.objects.create(
                animal=instance,
                ration_table=default_ration_table,
                start_date=instance.created_at,
                is_active=True
            )
            print(f"Default ration assigned to animal {instance.eartag}.")
        else:
            print("Default ration table not found. Please create one.")

### signal for ending ration log for animal 
@receiver(post_save, sender=Animal)
def handle_slaughtered_animal(sender, instance, **kwargs):
    # Check if the animal is slaughtered
    if instance.is_slaughtered:
        try:
            # Get the most recent active ration log for this animal
            last_active_log = AnimalRationLog.objects.filter(animal=instance, is_active=True).latest('start_date')

            # Update end_date and deactivate the log
            last_active_log.end_date = now()
            last_active_log.is_active = False
            last_active_log.save()

        except AnimalRationLog.DoesNotExist:
            # No active ration logs found
            print(f"No active ration logs found for animal {instance.eartag}.")