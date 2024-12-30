from django.db import models
from django.utils.timezone import now
from .managers import ActiveManager


class RationComponent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dry_matter = models.DecimalField(max_digits=5, decimal_places=2, help_text="Dry matter percentage")
    calori = models.DecimalField(max_digits=5, decimal_places=2)
    nisasta = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Add soft delete field

     # Attach custom managers
    objects = ActiveManager()  # Default manager excludes soft-deleted records
    all_objects = models.Manager()  # Includes all records

    def delete(self, *args, **kwargs):
        # Soft delete by setting deleted_at
        self.deleted_at = now()
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    def __str__(self):
        return self.name

class RationTable(models.Model):
    name = models.CharField(max_length=255)
    components = models.ManyToManyField(RationComponent, through='RationTableComponent')
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compute_cost(self):
        return sum(
            component.quantity * component.component.price
            for component in self.rationtablecomponent_set.all()
        )

    def __str__(self):
        return self.name


class RationTableComponent(models.Model):
    ration_table = models.ForeignKey(RationTable, on_delete=models.CASCADE)
    component = models.ForeignKey(RationComponent, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('ration_table', 'component')

    def __str__(self):
        return f"{self.ration_table.name} - {self.component.name}"
