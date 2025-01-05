from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ration_components.models import RationComponent, RationTable, RationTableComponent
from ration_logs.models import ComponentChangeLog, RationTableLog, RationTableComponentLog
from django.utils.timezone import now


class RationComponentsIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample RationComponent
        self.component = RationComponent.objects.create(
            name="Sample Component",
            description="A test component",
            dry_matter=85.0,
            calori=12.5,
            nisasta=45.0,
            price=100.0,
        )

        # Create sample RationTable
        self.table = RationTable.objects.create(
            name="Sample Table",
            description="A test ration table",
        )

        # Create sample RationTableComponent
        self.table_component = RationTableComponent.objects.create(
            ration_table=self.table,
            component=self.component,
            quantity=10.0,
        )

    def test_create_ration_component_and_log(self):
        """Test creating a RationComponent and logging the initial values."""
        response = self.client.post(
            "/api/ration-components/",
            {
                "name": "New Component",
                "description": "A new test component",
                "dry_matter": 80.0,
                "calori": 10.0,
                "nisasta": 50.0,
                "price": 200.0,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        component_id = response.data["id"]
        logs = ComponentChangeLog.objects.filter(component_id=component_id)
        self.assertEqual(logs.count(), 4)  # Logs for price, dry_matter, calori, nisasta

    def test_soft_delete_ration_component_and_log(self):
        """Test soft-deleting a RationComponent and creating a log."""
        response = self.client.delete(f"/api/ration-components/{self.component.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        log = ComponentChangeLog.objects.filter(
            component=self.component, field_name="deleted_at"
        ).last()
        self.assertIsNotNone(log)
        self.assertIsNotNone(log.new_value)

    def test_restore_ration_component_and_log(self):
        """Test restoring a soft-deleted RationComponent and logging the restoration."""
        self.component.delete()
        response = self.client.post(f"/api/ration-components/{self.component.id}/restore/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = ComponentChangeLog.objects.filter(
            component=self.component, field_name="deleted_at"
        ).last()
        self.assertIsNotNone(log)
        self.assertIsNone(log.new_value)

    def test_create_ration_table_and_log(self):
        """Test creating a RationTable and logging the creation."""
        response = self.client.post(
            "/api/ration-tables/",
            {"name": "New Table", "description": "A new test table"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        table_id = response.data["id"]
        logs = RationTableLog.objects.filter(ration_table_id=table_id, action="Created")
        self.assertEqual(logs.count(), 1)

    def test_soft_delete_ration_table_and_log(self):
        """Test soft-deleting a RationTable and creating a log."""
        response = self.client.delete(f"/api/ration-tables/{self.table.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        log = RationTableLog.objects.filter(ration_table=self.table, action="Soft Deleted").last()
        self.assertIsNotNone(log)

    def test_restore_ration_table_and_log(self):
        """Test restoring a soft-deleted RationTable and logging the restoration."""
        self.table.delete()
        response = self.client.post(f"/api/ration-tables/{self.table.id}/restore/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = RationTableLog.objects.filter(ration_table=self.table, action="Restored").last()
        self.assertIsNotNone(log)

    def test_create_ration_table_component_and_log(self):
        """Test creating a RationTableComponent and logging the creation."""
        response = self.client.post(
            "/api/ration-table-components/",
            {
                "ration_table": self.ration_table.id,  # Ensure this ID is unique in combination
                "component": self.component.id + 1,   # Use a different component ID
                "quantity": 15.0,
            },
        )
        print("Response JSON:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        table_component_id = response.data["id"]
        logs = RationTableComponentLog.objects.filter(
            table_component_id=table_component_id, action="Created"
        )
        self.assertEqual(logs.count(), 1)

    def test_update_ration_table_component_and_log(self):
        """Test updating a RationTableComponent quantity and logging the update."""
        response = self.client.patch(
            f"/api/ration-table-components/{self.table_component.id}/",
            {"quantity": 20.0},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = RationTableComponentLog.objects.filter(
            table_component=self.table_component, action="Updated"
        ).last()
        self.assertIsNotNone(log)
        self.assertEqual(log.old_quantity, 10.0)
        self.assertEqual(log.new_quantity, 20.0)

    def test_soft_delete_ration_table_component_and_log(self):
        """Test soft-deleting a RationTableComponent and creating a log."""
        response = self.client.delete(f"/api/ration-table-components/{self.table_component.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        log = RationTableComponentLog.objects.filter(
            table_component=self.table_component, action="Soft Deleted"
        ).last()
        self.assertIsNotNone(log)

    def test_restore_ration_table_component_and_log(self):
        """Test restoring a soft-deleted RationTableComponent and logging the restoration."""
        self.table_component.delete()
        response = self.client.post(f"/api/ration-table-components/{self.table_component.id}/restore/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = RationTableComponentLog.objects.filter(
            table_component=self.table_component, action="Restored"
        ).last()
        self.assertIsNotNone(log)
