from django.db.models.signals import post_save
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
