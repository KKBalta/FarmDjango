from django.db.models.signals import post_save
from django.utils.timezone import now
from django.dispatch import receiver
from animal_ration.models import AnimalRationLog
from ration_components.models import RationTable
from .models import Animal  # Import the Animal model
from django.conf import settings

@receiver(post_save, sender=Animal)
def assign_default_ration(sender, instance, created, **kwargs):
    if created:  # Only assign when a new animal is created
        default_ration_table_name = getattr(settings, 'DEFAULT_RATION_NAME', 'Base Ration')
        default_ration_table = RationTable.objects.filter(name=default_ration_table_name).first()

        if default_ration_table:
            AnimalRationLog.objects.create(
                animal=instance,
                ration_table=default_ration_table,
                start_date=now(),
                is_active=True
            )
            print(f"Default ration '{default_ration_table_name}' assigned to animal {instance.eartag}.")
        else:
            print(f"Default ration '{default_ration_table_name}' not found. Please create one.")


### signal for ending ration log for animal 
@receiver(post_save, sender=Animal)
def handle_slaughtered_animal(sender, instance, **kwargs):
    if instance.is_slaughtered:
        try:
            # Fetch the active ration log for the animal
            last_active_log = AnimalRationLog.objects.filter(
                animal=instance,
                is_active=True
            ).latest('start_date')

            # Deactivate the ration log
            last_active_log.end_date = now()
            last_active_log.is_active = False
            last_active_log.save()

            print(f"Ration log ended for slaughtered animal {instance.eartag}.")
        except AnimalRationLog.DoesNotExist:
            print(f"No active ration log found for animal {instance.eartag}.")
