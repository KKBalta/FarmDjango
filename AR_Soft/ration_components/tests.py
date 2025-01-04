from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import RationComponent, RationTable, RationTableComponent


class RationComponentTestCase(TestCase):
    """Test cases for RationComponent API functionality."""

    def setUp(self):
        self.client = APIClient()
        self.component1 = RationComponent.objects.create(
            name="Component 1",
            description="Test Component 1",
            dry_matter=85.5,
            calori=12.5,
            nisasta=45.2,
            price=100.00,
        )
        self.component2 = RationComponent.objects.create(
            name="Component 2",
            description="Test Component 2",
            dry_matter=90.0,
            calori=15.0,
            nisasta=50.0,
            price=120.00,
        )

    def test_soft_delete_component(self):
        response = self.client.delete(f"/api/ration-components/{self.component1.id}/")
        self.component1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.component1.is_deleted())

    def test_restore_soft_deleted_component(self):
        self.component1.delete()
        response = self.client.post(f"/api/ration-components/{self.component1.id}/restore/")
        self.component1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.component1.is_deleted())

    def test_hard_delete_component(self):
        self.component1.delete()
        response = self.client.delete(f"/api/ration-components/{self.component1.id}/hard-delete/")
        with self.assertRaises(RationComponent.DoesNotExist):
            RationComponent.all_objects.get(id=self.component1.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_soft_deleted_components(self):
        self.component1.delete()
        response = self.client.get("/api/ration-components/soft-deleted/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.component1.id)

    def test_edge_case_restore_active_component(self):
        response = self.client.post(f"/api/ration-components/{self.component1.id}/restore/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not deleted", response.data["status"])

    def test_edge_case_hard_delete_active_component(self):
        response = self.client.delete(f"/api/ration-components/{self.component1.id}/hard-delete/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not soft deleted", response.data["status"])


class RationTableTestCase(TestCase):
    """Test cases for RationTable API functionality."""

    def setUp(self):
        self.client = APIClient()
        self.component = RationComponent.objects.create(
            name="Test Component",
            dry_matter=85.5,
            calori=12.5,
            nisasta=45.2,
            price=100.00,
        )
        self.table = RationTable.objects.create(
            name="Test Table",
            description="Test Description",
        )
        RationTableComponent.objects.create(
            ration_table=self.table,
            component=self.component,
            quantity=10.0,
        )

    def test_soft_delete_ration_table(self):
        response = self.client.delete(f"/api/ration-tables/{self.table.id}/")
        self.table.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.table.is_deleted())

    def test_restore_ration_table(self):
        self.table.delete()
        response = self.client.post(f"/api/ration-tables/{self.table.id}/restore/")
        self.table.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.table.is_deleted())

    def test_hard_delete_ration_table(self):
        self.table.delete()
        response = self.client.delete(f"/api/ration-tables/{self.table.id}/hard-delete/")
        with self.assertRaises(RationTable.DoesNotExist):
            RationTable.all_objects.get(id=self.table.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_compute_cost(self):
        response = self.client.get(f"/api/ration-tables/{self.table.id}/compute-cost/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cost"], 1000.0)


class RationTableComponentTestCase(TestCase):
    """Test cases for RationTableComponent API functionality."""

    def setUp(self):
        self.client = APIClient()
        self.component = RationComponent.objects.create(
            name="Test Component",
            dry_matter=85.5,
            calori=12.5,
            nisasta=45.2,
            price=100.00,
        )
        self.table = RationTable.objects.create(
            name="Test Table",
            description="Test Description",
        )
        self.table_component = RationTableComponent.objects.create(
            ration_table=self.table,
            component=self.component,
            quantity=10.0,
        )

    def test_soft_delete_table_component(self):
        response = self.client.delete(f"/api/ration-table-components/{self.table_component.id}/")
        self.table_component.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.table_component.is_deleted())

    def test_restore_table_component(self):
        self.table_component.delete()
        response = self.client.post(f"/api/ration-table-components/{self.table_component.id}/restore/")
        self.table_component.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.table_component.is_deleted())

    def test_hard_delete_table_component(self):
        self.table_component.delete()
        response = self.client.delete(f"/api/ration-table-components/{self.table_component.id}/hard-delete/")
        with self.assertRaises(RationTableComponent.DoesNotExist):
            RationTableComponent.all_objects.get(id=self.table_component.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
