from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import RationTableComponent, RationTable


@receiver(post_save, sender=RationTableComponent)
def log_table_component_save(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    print(f"Component '{instance.component.name}' in table '{instance.ration_table.name}' was {action.lower()}.")


@receiver(post_delete, sender=RationTableComponent)
def log_table_component_delete(sender, instance, **kwargs):
    print(f"Component '{instance.component.name}' removed from table '{instance.ration_table.name}'.")
