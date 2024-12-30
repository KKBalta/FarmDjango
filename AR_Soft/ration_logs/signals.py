from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from ration_components.models import RationComponent, RationTable, RationTableComponent
from .models import ComponentChangeLog, RationTableLog, RationTableComponentLog

# Signal for RationComponent updates
@receiver(pre_save, sender=RationComponent)
def log_component_update(sender, instance, **kwargs):
    # Fetch the old instance before saving
    old_instance = instance.__class__.objects.filter(pk=instance.pk).first()
    if not old_instance:
        print("No old instance found; skipping update logging.")
        return

    print(f"Checking for updates to fields in component {instance.name}")
    for field in ['price', 'dry_matter', 'calori', 'nisasta']:
        old_value = getattr(old_instance, field, None)
        new_value = getattr(instance, field, None)
        print(f"Comparing field '{field}': old_value={old_value}, new_value={new_value}")
        if old_value != new_value:
            print(f"Field '{field}' changed: {old_value} -> {new_value}")
            ComponentChangeLog.objects.create(
                component=instance,
                field_name=field,
                old_value=old_value,
                new_value=new_value,
            )

# Signal for RationComponent creation
@receiver(post_save, sender=RationComponent)
def log_component_creation(sender, instance, created, **kwargs):
    if created:  # Log creation only
        print(f"Component created: {instance.name}")
        # Create logs for each field with its base value
        for field in ['price', 'dry_matter', 'calori', 'nisasta']:
            base_value = getattr(instance, field, None)
            ComponentChangeLog.objects.create(
                component=instance,
                field_name=field,
                old_value=None,  # No previous value
                new_value=base_value,  # Base value at creation
            )


# Signal for RationComponent deletion
@receiver(post_delete, sender=RationComponent)
def log_component_deletion(sender, instance, **kwargs):
    print(f"Component deleted: {instance.name}")
    # Create logs for each field with its final value
    for field in ['price', 'dry_matter', 'calori', 'nisasta']:
        last_value = getattr(instance, field, None)
        ComponentChangeLog.objects.create(
            component=instance,
            field_name=field,
            old_value=last_value,  # The value before deletion
            new_value=None,  # No new value because the object is deleted
        )


# Signal for RationTable creation and updates
@receiver(post_save, sender=RationTable)
def log_ration_table_creation_or_update(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    print(f"RationTable {action}: {instance.name}")
    RationTableLog.objects.create(
        ration_table=instance,
        action=action,
    )

# Signal for RationTable deletion
@receiver(post_delete, sender=RationTable)
def log_ration_table_deletion(sender, instance, **kwargs):
    print(f"RationTable deleted: {instance.name}")
    RationTableLog.objects.create(
        ration_table=instance,
        action="Deleted",
    )

# Signal for RationTableComponent updates
@receiver(pre_save, sender=RationTableComponent)
def log_table_component_update(sender, instance, **kwargs):
    if instance.pk:  # Log updates
        old_instance = RationTableComponent.objects.get(pk=instance.pk)
        if old_instance.quantity != instance.quantity:
            print(f"RationTableComponent updated: {instance.component.name} in {instance.ration_table.name}")
            RationTableComponentLog.objects.create(
                table_component=instance,
                action="Updated",
                old_quantity=old_instance.quantity,
                new_quantity=instance.quantity,
            )

# Signal for RationTableComponent creation
@receiver(post_save, sender=RationTableComponent)
def log_table_component_creation(sender, instance, created, **kwargs):
    if created:  # Log creation
        print(f"RationTableComponent created: {instance.component.name} in {instance.ration_table.name}")
        RationTableComponentLog.objects.create(
            table_component=instance,
            action="Created",
            new_quantity=instance.quantity,
        )

# Signal for RationTableComponent deletion
@receiver(post_delete, sender=RationTableComponent)
def log_table_component_deletion(sender, instance, **kwargs):
    print(f"RationTableComponent deleted: {instance.component.name} from {instance.ration_table.name}")
    RationTableComponentLog.objects.create(
        table_component=instance,
        action="Deleted",
        old_quantity=instance.quantity,
    )
