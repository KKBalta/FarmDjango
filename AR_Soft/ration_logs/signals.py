from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from ration_components.models import RationComponent, RationTable, RationTableComponent
from .models import ComponentChangeLog, RationTableLog, RationTableComponentLog

# Signal for RationComponent changes
@receiver(pre_save, sender=RationComponent)
def log_component_changes(sender, instance, **kwargs):
    if instance.pk:  # Only log updates, not creation
        old_instance = RationComponent.objects.get(pk=instance.pk)
        for field in ['price', 'dry_matter', 'calori', 'nisasta']:
            old_value = getattr(old_instance, field)
            new_value = getattr(instance, field)
            if old_value != new_value:
                ComponentChangeLog.objects.create(
                    component=instance,
                    field_name=field,
                    old_value=old_value,
                    new_value=new_value,
                )

# Signal for RationTable changes
@receiver(post_save, sender=RationTable)
def log_ration_table_changes(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    RationTableLog.objects.create(
        ration_table=instance,
        action=action,
    )

@receiver(post_delete, sender=RationTable)
def log_ration_table_deletion(sender, instance, **kwargs):
    RationTableLog.objects.create(
        ration_table=instance,
        action="Deleted",
    )

# Signal for RationTableComponent changes
@receiver(pre_save, sender=RationTableComponent)
def log_table_component_changes(sender, instance, **kwargs):
    if instance.pk:  # Log updates
        old_instance = RationTableComponent.objects.get(pk=instance.pk)
        if old_instance.quantity != instance.quantity:
            RationTableComponentLog.objects.create(
                table_component=instance,
                action="Updated",
                old_quantity=old_instance.quantity,
                new_quantity=instance.quantity,
            )

@receiver(post_save, sender=RationTableComponent)
def log_table_component_creation(sender, instance, created, **kwargs):
    if created:  # Log creation
        RationTableComponentLog.objects.create(
            table_component=instance,
            action="Created",
            new_quantity=instance.quantity,
        )

@receiver(post_delete, sender=RationTableComponent)
def log_table_component_deletion(sender, instance, **kwargs):
    RationTableComponentLog.objects.create(
        table_component=instance,
        action="Deleted",
        old_quantity=instance.quantity,
    )
