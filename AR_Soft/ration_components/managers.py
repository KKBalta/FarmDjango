from django.db import models

class ActiveManager(models.Manager):
    def get_queryset(self):
        # Exclude soft-deleted records
        return super().get_queryset().filter(deleted_at__isnull=True)
