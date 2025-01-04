from django.test import TestCase
from django.utils.timezone import make_aware, datetime, timedelta, is_naive, now
from ration_components.models import RationComponent, RationTable, RationTableComponent
from animal_ration.models import AnimalRationLog
from Animal.models import Animal
from Farmer.models import Company


class FeedCostTestWithMockData(TestCase):
    def setUp(self):
        # Create a company and an animal
        self.company = Company.objects.create(name="FarmCo")
        self.animal = Animal.objects.create(
            eartag="12345", company=self.company, race="Holstein", gender=True, room="Barn 1", cost=1200.00
        )

        # Create ration tables and components
        self.ration_table = RationTable.objects.create(name="kis tablosu")
        self.component_arpa = RationComponent.objects.create(
            name="arpa", price=35.00, dry_matter=10.10, calori=213.00, nisasta=31.00
        )
        self.component_atk = RationComponent.objects.create(
            name="ATK", price=20.00, dry_matter=12.00, calori=180.00, nisasta=15.00
        )

        # Add components to the ration table
        self.arpa_component = RationTableComponent.objects.create(
            ration_table=self.ration_table, component=self.component_arpa, quantity=2.0
        )
        self.atk_component = RationTableComponent.objects.create(
            ration_table=self.ration_table, component=self.component_atk, quantity=2.15
        )

        # Create ration logs for the animal
        self.ration_log = AnimalRationLog.objects.create(
            animal=self.animal,
            ration_table=self.ration_table,
            start_date=make_aware(datetime(2024, 12, 20, 0, 0)),  # Ensure timezone-awareness
            end_date=None
        )

        # Create changes for the components
        changes = [
            {
                "ration_table_component_id": None,
                "ration_table_name": "arpa",
                "component_name": "arpa",
                "action": "UPDATED",
                "old_price": 35.00,
                "new_price": 46.00,
                "changed_at": make_aware(datetime(2024, 12, 23, 11, 13, 50))
            },
            {
                "ration_table_component_id": None,
                "ration_table_name": "arpa",
                "component_name": "arpa",
                "action": "UPDATED",
                "old_price": 46.00,
                "new_price": 50.00,
                "changed_at": make_aware(datetime(2024, 12, 26, 13, 29, 44))
            },
            {
                "ration_table_component_id": 6,
                "ration_table_name": "kis tablosu",
                "component_name": "ATK",
                "action": "UPDATED",
                "old_quantity": 2.15,
                "new_quantity": 2.35,
                "changed_at": make_aware(datetime(2024, 12, 27, 6, 49, 18))
            },
        ]

        for change in changes:
            RationComponentChange.objects.create(
                ration_table_component_id=change["ration_table_component_id"],
                ration_table_name=change["ration_table_name"],
                component_name=change["component_name"],
                action=change["action"],
                old_price=change.get("old_price"),
                new_price=change.get("new_price"),
                old_dry_matter=change.get("old_dry_matter"),
                new_dry_matter=change.get("new_dry_matter"),
                old_calori=change.get("old_calori"),
                new_calori=change.get("new_calori"),
                old_nisasta=change.get("old_nisasta"),
                new_nisasta=change.get("new_nisasta"),
                changed_at=change["changed_at"],
            )

    from django.utils.timezone import is_naive, now

def test_feed_cost_calculation_with_created_at(self):
    """
    Test feed cost calculation using the animal's created_at as start_date.
    """
    animal = self.animal  # Assume the animal is set up in the test's setUp method
    
    # Ensure start_date is timezone-aware
    start_date = animal.created_at if not is_naive(animal.created_at) else make_aware(animal.created_at)
    
    # Ensure end_date is timezone-aware
    end_date = now()

    # Calculate feed cost
    feed_cost = animal.calculate_feed_cost(start_date, end_date)

    # Print the result for debugging
    print(f"Feed cost for animal '{animal.eartag}' from {start_date} to {end_date}: {feed_cost}")

    # Expected cost (manually calculated based on test data)
    expected_cost = 220.00  # Replace with the actual expected value based on your setup
    self.assertAlmostEqual(feed_cost, expected_cost, places=2, msg="Feed cost calculation failed.")
