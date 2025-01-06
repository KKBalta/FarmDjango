from django.db import models
from django.utils.timezone import now
from .manager import ActiveManager
from decimal import Decimal

class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, hard_delete=False, **kwargs):
        if hard_delete:
            super().delete(*args, **kwargs)  # This should remove the record from the database
        else:
            self.deleted_at = now()
            self.save()


    def restore(self, *args, **kwargs):
        # Restore soft-deleted object
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

class RationComponent(SoftDeleteModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dry_matter = models.DecimalField(max_digits=5, decimal_places=2, help_text="Dry matter percentage")
    calori = models.DecimalField(max_digits=5, decimal_places=2)
    nisasta = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveManager()  # Default manager excludes soft-deleted records
    all_objects = models.Manager()  # Includes all records

    def delete(self, *args, hard_delete=False, **kwargs):
        # Call parent delete for core functionality
        super().delete(*args, hard_delete=hard_delete, **kwargs)

        # Additional logic for soft delete
        if not hard_delete:
            self.rationtablecomponent_set.update(deleted_at=now())

    def restore(self, *args, **kwargs):
        # Call parent restore for core functionality
        super().restore(*args, **kwargs)

        # Additional logic for restore
        self.rationtablecomponent_set.update(deleted_at=None)

    def __str__(self):
        return self.name
    
class RationTable(SoftDeleteModel):
    name = models.CharField(max_length=255)
    components = models.ManyToManyField(RationComponent, through='RationTableComponent')
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Managers
    objects = ActiveManager()  # Default manager for active records
    all_objects = models.Manager()  # Includes soft-deleted records

    def delete(self, *args, hard_delete=False, **kwargs):
        # Call parent delete for core functionality
        super().delete(*args, hard_delete=hard_delete, **kwargs)

        # Additional logic for soft delete
        if not hard_delete:
            self.rationtablecomponent_set.update(deleted_at=now())

    def restore(self, *args, **kwargs):
        # Call parent restore for core functionality
        super().restore(*args, **kwargs)

        # Additional logic for restore
        self.rationtablecomponent_set.update(deleted_at=None)

    def compute_cost(self):
        return sum(
            component.quantity * component.component.price
            for component in self.rationtablecomponent_set.all()
        )
    def compute_total_dry_matter(self):
        """Compute the total dry matter of the ration table."""
        return sum(
            Decimal(component.component.dry_matter) * Decimal(component.quantity)
            for component in self.rationtablecomponent_set.all()
        )
    def compute_total_calori(self):
        """Compute the total calori of the ration table."""
        return sum(
            Decimal(component.component.calori) * Decimal(component.quantity)
            for component in self.rationtablecomponent_set.all()
        )

    def compute_total_nisasta(self):
        """Compute the total nisasta of the ration table."""
        return sum(
            Decimal(component.component.nisasta) * Decimal(component.quantity)
            for component in self.rationtablecomponent_set.all()
        )
    def __str__(self):
        return self.name

class RationTableComponent(models.Model):
    ration_table = models.ForeignKey('RationTable', on_delete=models.CASCADE)
    component = models.ForeignKey('RationComponent', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Managers
    objects = ActiveManager()  # Default manager for active records
    all_objects = models.Manager()  # Includes soft-deleted records

    class Meta:
        unique_together = ('ration_table', 'component')

    def delete(self, hard_delete=False, *args, **kwargs):
        if hard_delete:
            super().delete(*args, **kwargs)
        else:
            self.deleted_at = now()
            self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    def __str__(self):
        return f"{self.ration_table.name} - {self.component.name}"
