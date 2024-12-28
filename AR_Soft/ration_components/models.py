from django.db import models
from django.utils import timezone


class RationComponent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dry_matter = models.DecimalField(max_digits=5, decimal_places=2, help_text="Dry matter percentage of the component", null=False, blank=False)
    calori = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    nisasta = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)

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
    component = models.ForeignKey(RationComponent, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('ration_table', 'component')

    def __str__(self):
        return f"{self.ration_table.name} - {self.component.name}"

    def calculate_dry_matter(self):
        return self.quantity * (self.component.dry_matter / 100)