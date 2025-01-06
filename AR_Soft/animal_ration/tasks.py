from celery import shared_task
from animal_ration.models import AnimalRationLog
from Animal.models import Animal, AnimalGroup
from ration_components.models import RationTableComponent
from django.db.models import Sum
import logging
from decimal import Decimal, ROUND_HALF_UP
from Weight.models import Weight

logger = logging.getLogger(__name__)

from decimal import Decimal

@shared_task
def update_feed_costs():
    logs = AnimalRationLog.objects.filter(is_active=True).select_related('animal', 'ration_table')
    print(f"Processing {logs.count()} active ration logs.")
    
    for log in logs:
        animal = log.animal

        # Fetch the first active AnimalGroup for the animal
        animal_group = AnimalGroup.objects.filter(animal=animal).select_related('group').first()
        if not animal_group:
            print(f"Animal {animal.eartag} is not assigned to any group. Skipping.")
            continue

        group = animal_group.group  # Access the associated Group
        if not group.dry_matter:
            print(f"Group {group.name} for Animal {animal.eartag} has no dry matter value. Skipping.")
            continue

        # Get the most recent weight of the animal
        weight_record = Weight.objects.filter(animal=animal).order_by('-recorded_at').first()
        if not weight_record:
            print(f"No weight record found for Animal {animal.eartag}. Skipping.")
            continue

        current_weight = Decimal(weight_record.weight).quantize(Decimal('0.00000'), rounding=ROUND_HALF_UP)
        print(f"Animal {animal.eartag} Current Weight: {current_weight} kg, Type: {type(current_weight)}")

        # Convert `dry_matter` to Decimal to match other calculations
        dm = Decimal(group.dry_matter).quantize(Decimal('0.00000'), rounding=ROUND_HALF_UP) * current_weight
        print(f"Group DM: {dm}, Type: {type(dm)}")

        # Get the ration table and calculate daily cost
        ration_table = log.ration_table
        daily_cost = Decimal(ration_table.compute_cost())
        print(f"Daily Cost: {daily_cost}, Type: {type(daily_cost)}")

        # Use the compute_total_dry_matter method from the RationTable model
        table_dm = Decimal(ration_table.compute_total_dry_matter())
        print(f"Table DM (with quantity): {table_dm}, Type: {type(table_dm)}")

        if not table_dm or table_dm == 0:
            print(f"Ration table {ration_table.name} has no valid dry matter value. Skipping animal {animal.eartag}.")
            continue

        # Calculate the feed cost for the animal
        animal_feed_cost = daily_cost * (dm / table_dm)
        print(f"Animal Feed Cost: {animal_feed_cost}")

        # Update and save the animal's feed cost
        animal.feed_cost += animal_feed_cost
        animal.save()

        print(f"Updated feed cost for {animal.eartag}: {animal.feed_cost}")

    return f"Updated feed costs for {logs.count()} animals."

@shared_task
def test_task():
    print("Test task executed successfully!")
    return "Hello from Celery"
