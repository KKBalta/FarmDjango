from django.db import models
from django.utils import timezone  


class RationComponent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class RationTable(models.Model):
    name = models.CharField(max_length=255)
    components = models.ManyToManyField(RationComponent, through='RationTableComponent')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class RationTableComponent(models.Model):
    ration_table = models.ForeignKey(RationTable, on_delete=models.CASCADE)
    component = models.ForeignKey(RationComponent, on_delete=models.PROTECT)  # Prevent deletion if referenced
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('ration_table', 'component')

    def __str__(self):
        return f"{self.ration_table.name} - {self.component.name}"


class RationComponentChange(models.Model):
    ACTION_CHOICES = [
        ('CREATED', 'Created'),
        ('UPDATED', 'Updated'),
        ('DELETED', 'Deleted'),
    ]

    ration_table_component_id = models.IntegerField()  # Keep the ID even if the entry is deleted
    ration_table_name = models.CharField(max_length=255)  # Preserve the table name
    component_name = models.CharField(max_length=255)  # Preserve the component name
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)  # Log the action
    old_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    changed_at = models.DateTimeField(default=timezone.now)  # Auto-add timestamp

    def __str__(self):
        return f"{self.action} on {self.component_name} in {self.ration_table_name} at {self.changed_at}"
