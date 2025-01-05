from django.db import models
from django.utils.timezone import now

# Log for RationComponent changes
class ComponentChangeLog(models.Model):
    component = models.ForeignKey(
        'ration_components.RationComponent',
        on_delete=models.CASCADE,
        related_name='change_logs'
    )
    field_name = models.CharField(max_length=50)  # E.g., 'price', 'calorie', 'deleted_at'
    old_value = models.TextField(null=True, blank=True)  # Use TextField for mixed data types
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change in {self.component.name} ({self.field_name})"
    
# Log for RationTable changes
class RationTableLog(models.Model):
    ration_table = models.ForeignKey(
        'ration_components.RationTable', 
        on_delete=models.CASCADE, 
        related_name='logs'
    )
    action = models.CharField(max_length=50)  # 'Created', 'Updated', 'Deleted'
    description = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.action} - {self.ration_table.name}"

# Log for RationTableComponent changes
class RationTableComponentLog(models.Model):
    table_component = models.ForeignKey(
        'ration_components.RationTableComponent', 
        on_delete=models.CASCADE, 
        related_name='logs'
    )
    action = models.CharField(max_length=50)  # 'Created', 'Updated', 'Deleted'
    old_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    changed_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.action} - {self.table_component}"
