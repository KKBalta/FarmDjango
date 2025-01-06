from django.test import TestCase
from django.utils.timezone import now
from Animal.models import Animal
from Slaughter.models import Slaughter
from Farmer.models import Company


class SlaughterModelTests(TestCase):
    def setUp(self):
        # Create a test company
        self.company = Company.objects.create(name="Test Farm")

        # Create a test animal
        self.animal = Animal.objects.create(
            eartag="12345",
            company=self.company,
            race="Test Breed",
            gender=True,
            room="Room A",
            cost=200.0,
            feed_cost=50.0,
        )

        # Create a test slaughter record
        self.slaughter = Slaughter.objects.create(
            animal=self.animal,
            carcas_weight=250.0,
            sale_price=500.0,
            kdv=0.18,  # 18% tax
            date=now(),
        )

    def test_calculate_profit(self):
        """
        Test the profit calculation for a slaughter entry.
        """
        expected_profit = (self.slaughter.sale_price * self.slaughter.carcas_weight) - (
            self.animal.cost
            + self.animal.feed_cost
            + (self.slaughter.sale_price * self.slaughter.carcas_weight * self.slaughter.kdv)
        )
        self.assertAlmostEqual(self.slaughter.calculate_profit(), expected_profit)

    def test_animal_marked_as_slaughtered(self):
        """
        Test that the related animal is marked as slaughtered upon creating a Slaughter record.
        """
        self.assertTrue(self.animal.is_slaughtered)

    def test_slaughter_str_representation(self):
        """
        Test the string representation of a slaughter record.
        """
        expected_str = f"{self.animal.eartag} - {self.slaughter.carcas_weight}kg on {self.slaughter.date}"
        self.assertEqual(str(self.slaughter), expected_str)


class SlaughterAPITests(TestCase):
    def setUp(self):
        # Create a test company
        self.company = Company.objects.create(name="Test Farm")

        # Create a test animal
        self.animal = Animal.objects.create(
            eartag="12345",
            company=self.company,
            race="Test Breed",
            gender=True,
            room="Room A",
            cost=200.0,
            feed_cost=50.0,
        )

        # Create a test slaughter record
        self.slaughter = Slaughter.objects.create(
            animal=self.animal,
            carcas_weight=250.0,
            sale_price=500.0,
            kdv=0.18,
            date=now(),
        )

    def test_get_slaughter_list(self):
        """
        Test the GET request for retrieving a list of slaughter records.
        """
        response = self.client.get("/api/slaughters/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_slaughter_detail(self):
        """
        Test the GET request for retrieving a single slaughter record.
        """
        response = self.client.get(f"/api/slaughters/{self.slaughter.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["animal"], self.animal.id)

    def test_post_slaughter(self):
        """
        Test the POST request for creating a new slaughter record.
        """
        data = {
            "animal": self.animal.id,
            "carcas_weight": 300.0,
            "sale_price": 600.0,
            "kdv": 0.18,
        }
        response = self.client.post("/api/slaughters/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Slaughter.objects.filter(carcas_weight=300.0).exists())

    def test_total_profit_endpoint(self):
        """
        Test the total profit calculation endpoint.
        """
        response = self.client.get("/api/slaughters/total-profit/")
        self.assertEqual(response.status_code, 200)
        expected_total_profit = (
            (self.slaughter.sale_price * self.slaughter.carcas_weight)
            - (
                self.animal.cost
                + self.animal.feed_cost
                + (self.slaughter.sale_price * self.slaughter.carcas_weight * self.slaughter.kdv)
            )
        )
        self.assertAlmostEqual(response.json()["total_profit"], expected_total_profit)
