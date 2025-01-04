from django.db import models

class ActiveManager(models.Manager):
    """Manager to filter out soft-deleted records."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
