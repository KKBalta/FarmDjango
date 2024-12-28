from django.core.management.base import BaseCommand
from Animal.models import Animal
from animal_ration.models import AnimalRationLog
from ration_components.models import RationTable

class Command(BaseCommand):
    help = "Assign Base Ration to all existing animals"

    def handle(self, *args, **kwargs):
        # Fetch the Base Ration table
        base_ration = RationTable.objects.filter(name="Base Ration").first()
        if not base_ration:
            self.stdout.write(self.style.ERROR("Base Ration table not found."))
            return

        # Get all animals that don't already have ration logs
        animals_without_ration = Animal.objects.filter(ration_logs__isnull=True)

        for animal in animals_without_ration:
            AnimalRationLog.objects.create(
                animal=animal,
                ration_table=base_ration,
                start_date=animal.created_at,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f"Assigned Base Ration to animal {animal.eartag}."))

        self.stdout.write(self.style.SUCCESS("Base Ration assignment complete."))
