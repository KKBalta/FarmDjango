from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ration_components.models import RationComponent, RationTable, RationTableComponent
from ration_logs.models import ComponentChangeLog, RationTableLog, RationTableComponentLog
from django.utils.timezone import now


def fetch_old_instance(sender, instance):
    """
    Fetch the old instance of a model using the `all_objects` manager.
    Return None if `all_objects` is not defined or the instance does not exist.
    """
    try:
        return sender.all_objects.filter(pk=instance.pk).first()
    except AttributeError:
        print(f"[WARNING] Model {sender.__name__} does not have 'all_objects' manager.")
        return None


# Signal for RationComponent updates
@receiver(pre_save, sender=RationComponent)
def log_component_update(sender, instance, **kwargs):
    old_instance = fetch_old_instance(sender, instance)
    if not old_instance:
        print(f"No old instance found; skipping update logging for {instance.name}.")
        return

    print(f"Checking for updates to fields in component {instance.name}")
    tracked_fields = ['price', 'dry_matter', 'calori', 'nisasta']
    for field in tracked_fields:
        old_value = getattr(old_instance, field, None)
        new_value = getattr(instance, field, None)
        if old_value != new_value:
            print(f"Field '{field}' changed: {old_value} -> {new_value}")
            ComponentChangeLog.objects.create(
                component=instance,
                field_name=field,
                old_value=old_value,
                new_value=new_value,
            )

    # Detect soft delete or restore
    if old_instance.deleted_at != instance.deleted_at:
        action = "Soft Deleted" if instance.deleted_at else "Restored"
        print(f"{action}: {instance.name}")
        ComponentChangeLog.objects.create(
            component=instance,
            field_name="deleted_at",
            old_value=str(old_instance.deleted_at) if old_instance.deleted_at else None,
            new_value=str(instance.deleted_at) if instance.deleted_at else None,
            changed_at=now(),
        )


# Signal for RationComponent creation
@receiver(post_save, sender=RationComponent)
def log_component_creation(sender, instance, created, **kwargs):
    if created:
        print(f"Component created: {instance.name}")
        tracked_fields = ['price', 'dry_matter', 'calori', 'nisasta']
        for field in tracked_fields:
            base_value = getattr(instance, field, None)
            ComponentChangeLog.objects.create(
                component=instance,
                field_name=field,
                old_value=None,
                new_value=base_value,
            )


# Signal for RationTable creation and updates
@receiver(post_save, sender=RationTable)
def log_ration_table_creation_or_update(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    print(f"RationTable {action}: {instance.name}")
    RationTableLog.objects.create(
        ration_table=instance,
        action=action,
        description=f"RationTable {action.lower()}d.",
        changed_at=now(),
    )


# Signal for RationTable soft delete or restore
@receiver(pre_save, sender=RationTable)
def log_ration_table_soft_delete_restore(sender, instance, **kwargs):
    old_instance = fetch_old_instance(sender, instance)
    if not old_instance:
        return

    if old_instance.deleted_at != instance.deleted_at:
        action = "Soft Deleted" if instance.deleted_at else "Restored"
        print(f"{action} RationTable: {instance.name}")
        RationTableLog.objects.create(
            ration_table=instance,
            action=action,
            description=f"RationTable {action.lower()}.",
            changed_at=now(),
        )


# Signal for RationTableComponent creation
@receiver(post_save, sender=RationTableComponent)
def log_table_component_creation(sender, instance, created, **kwargs):
    if created:
        print(f"RationTableComponent created: {instance.component.name} in {instance.ration_table.name}")
        RationTableComponentLog.objects.create(
            table_component=instance,
            action="Created",
            new_quantity=instance.quantity,
        )


# Signal for RationTableComponent updates
@receiver(pre_save, sender=RationTableComponent)
def log_table_component_update(sender, instance, **kwargs):
    old_instance = fetch_old_instance(sender, instance)
    if not old_instance:
        return

    if old_instance.quantity != instance.quantity:
        print(f"RationTableComponent updated: {instance.component.name} in {instance.ration_table.name}")
        RationTableComponentLog.objects.create(
            table_component=instance,
            action="Updated",
            old_quantity=old_instance.quantity,
            new_quantity=instance.quantity,
        )

    # Detect soft delete or restore
    if old_instance.deleted_at != instance.deleted_at:
        action = "Soft Deleted" if instance.deleted_at else "Restored"
        print(f"{action} RationTableComponent: {instance.component.name}")
        RationTableComponentLog.objects.create(
            table_component=instance,
            action=action,
            old_quantity=None if action == "Soft Deleted" else instance.quantity,
            new_quantity=None if action == "Soft Deleted" else instance.quantity,
            changed_at=now(),
        )
from django.test import TestCase
from django.utils.timezone import now
from rest_framework.test import APIClient
from rest_framework import status
from ration_components.models import RationComponent, RationTable, RationTableComponent
from ration_logs.models import ComponentChangeLog, RationTableLog, RationTableComponentLog


class ComponentChangeLogTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.component = RationComponent.objects.create(
            name="Component 1",
            description="Test component",
            dry_matter=80.0,
            calori=10.0,
            nisasta=50.0,
            price=200.0,
        )

    def test_create_component_logs(self):
        logs = ComponentChangeLog.objects.filter(component=self.component)
        self.assertEqual(logs.count(), 4)  # One log per tracked field
        fields = {log.field_name for log in logs}
        self.assertSetEqual(fields, {"price", "dry_matter", "calori", "nisasta"})

    def test_update_component_logs(self):
        self.component.price = 250.0
        self.component.save()

        log = ComponentChangeLog.objects.filter(component=self.component, field_name="price").last()
        self.assertIsNotNone(log)
        self.assertEqual(log.old_value, "200.0")
        self.assertEqual(log.new_value, "250.0")

    def test_soft_delete_component_logs(self):
        self.component.delete()
        log = ComponentChangeLog.objects.filter(component=self.component, field_name="deleted_at").last()
        self.assertIsNotNone(log)
        self.assertEqual(log.old_value, None)
        self.assertIsNotNone(log.new_value)

    def test_restore_component_logs(self):
        self.component.delete()
        self.component.restore()

        log = ComponentChangeLog.objects.filter(component=self.component, field_name="deleted_at").last()
        self.assertIsNotNone(log)
        self.assertIsNotNone(log.old_value)
        self.assertEqual(log.new_value, None)


class RationTableLogTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.table = RationTable.objects.create(
            name="Test Table",
            description="Test description",
        )

    def test_create_ration_table_logs(self):
        logs = RationTableLog.objects.filter(ration_table=self.table)
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs.first().action, "Created")

    def test_update_ration_table_logs(self):
        self.table.description = "Updated description"
        self.table.save()

        logs = RationTableLog.objects.filter(ration_table=self.table, action="Updated")
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs.first().description, "RationTable updated.")

    def test_soft_delete_ration_table_logs(self):
        self.table.delete()
        log = RationTableLog.objects.filter(ration_table=self.table, action="Soft Deleted").last()
        self.assertIsNotNone(log)

    def test_restore_ration_table_logs(self):
        self.table.delete()
        self.table.restore()

        log = RationTableLog.objects.filter(ration_table=self.table, action="Restored").last()
        self.assertIsNotNone(log)


class RationTableComponentLogTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.component = RationComponent.objects.create(
            name="Component 1",
            description="Test component",
            dry_matter=80.0,
            calori=10.0,
            nisasta=50.0,
            price=200.0,
        )
        self.table = RationTable.objects.create(
            name="Test Table",
            description="Test description",
        )
        self.table_component = RationTableComponent.objects.create(
            ration_table=self.table,
            component=self.component,
            quantity=100.0,
        )

    def test_create_ration_table_component_logs(self):
        logs = RationTableComponentLog.objects.filter(table_component=self.table_component)
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs.first().action, "Created")
        self.assertEqual(logs.first().new_quantity, 100.0)

    def test_update_ration_table_component_logs(self):
        self.table_component.quantity = 150.0
        self.table_component.save()

        log = RationTableComponentLog.objects.filter(
            table_component=self.table_component, action="Updated"
        ).last()
        self.assertIsNotNone(log)
        self.assertEqual(log.old_quantity, 100.0)
        self.assertEqual(log.new_quantity, 150.0)

    def test_soft_delete_ration_table_component_logs(self):
        self.table_component.delete()
        log = RationTableComponentLog.objects.filter(
            table_component=self.table_component, action="Soft Deleted"
        ).last()
        self.assertIsNotNone(log)

    def test_restore_ration_table_component_logs(self):
        self.table_component.delete()
        self.table_component.restore()

        log = RationTableComponentLog.objects.filter(
            table_component=self.table_component, action="Restored"
        ).last()
        self.assertIsNotNone(log)


class APILogViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.component = RationComponent.objects.create(
            name="Component 1",
            description="Test component",
            dry_matter=80.0,
            calori=10.0,
            nisasta=50.0,
            price=200.0,
        )
        self.table = RationTable.objects.create(
            name="Test Table",
            description="Test description",
        )
        self.table_component = RationTableComponent.objects.create(
            ration_table=self.table,
            component=self.component,
            quantity=100.0,
        )

    def test_get_component_change_logs(self):
        response = self.client.get(f"/ration-logs/component-change-logs/component/{self.component.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_ration_table_logs(self):
        response = self.client.get(f"/ration-logs/ration-table-logs/table/{self.table.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_ration_table_component_logs(self):
        response = self.client.get(f"/ration-logs/ration-table-component-logs/table-component/{self.table_component.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
