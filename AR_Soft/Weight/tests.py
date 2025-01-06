from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from Animal.models import Animal, Group, AnimalGroup
from Farmer.models import Company
from Weight.models import Weight

class WeightModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")
        self.animal = Animal.objects.create(
            eartag="12345",
            company=self.company,
            race="Holstein",
            gender=True,
            room="Room A",
            cost=1500.0
        )
        self.weight1 = Weight.objects.create(animal=self.animal, weight=50.0, recorded_at=now() - timedelta(days=2))
        self.weight2 = Weight.objects.create(animal=self.animal, weight=55.0, recorded_at=now())

    def test_weight_creation(self):
        weight = Weight.objects.create(animal=self.animal, weight=60.0, recorded_at=now() + timedelta(days=1))
        self.assertEqual(weight.weight, 60.0)

    def test_unique_weight_per_date_constraint(self):
        with self.assertRaises(Exception):
            Weight.objects.create(animal=self.animal, weight=55.0, recorded_at=self.weight2.recorded_at)

    def test_string_representation(self):
        self.assertEqual(str(self.weight1), f"{self.animal.eartag} - {self.weight1.weight} kg on {self.weight1.recorded_at}")


class WeightAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name="Test Company")
        self.group = Group.objects.create(name="Test Group")
        self.animal = Animal.objects.create(
            eartag="12345",
            company=self.company,
            race="Holstein",
            gender=True,
            room="Room A",
            cost=1500.0
        )
        self.animal_group = AnimalGroup.objects.create(animal=self.animal, group=self.group)

        self.weight1 = Weight.objects.create(animal=self.animal, weight=50.0, recorded_at=now() - timedelta(days=2))
        self.weight2 = Weight.objects.create(animal=self.animal, weight=55.0, recorded_at=now())

    def test_get_weights(self):
        response = self.client.get("/api/weights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_weight(self):
        data = {
            "animal": self.animal.id,
            "weight": 60.0,
            "recorded_at": str(now())
        }
        print(f"Testing POST /api/weights/ with data: {data}")  # Debug: Print request payload

        response = self.client.post("/api/weights/", data)
        print(f"Response status code: {response.status_code}")  # Debug: Print response status code
        print(f"Response data: {response.data}")  # Debug: Print response data for debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_weight(self):
        data = {
            "animal": self.animal.id,
            "weight": 55.0,
            "recorded_at": str(self.weight2.recorded_at)
        }
        response = self.client.post("/api/weights/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_weight_detail(self):
        response = self.client.get(f"/api/weights/{self.weight1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["weight"], 50.0)

    def test_update_weight(self):
        data = {"weight": 52.0}
        response = self.client.patch(f"/api/weights/{self.weight1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["weight"], 52.0)

    def test_delete_weight(self):
        response = self.client.delete(f"/api/weights/{self.weight1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_daily_weight_gain(self):
        response = self.client.get(f"/api/weights/daily-gain/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("daily_gain", response.data)

    def test_all_weight_gain(self):
        response = self.client.get(f"/api/weights/all-gain/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["gain_history"]), 1)

    def test_group_daily_gain(self):
        response = self.client.get(f"/api/weights/group-daily-gain/{self.group.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_group_all_weight_gain(self):
        response = self.client.get(f"/api/weights/group-all-gain/{self.group.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
