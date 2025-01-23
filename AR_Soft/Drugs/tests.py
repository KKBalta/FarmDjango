from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from Animal.models import Animal  # Adjusted to match the correct app name
from Farmer.models import Company  # Import Company model for Animal creation
from Drugs.models import Vaccine, AnimalVaccineRecord


class VaccineModelTest(TestCase):
    def setUp(self):
        self.vaccine = Vaccine.objects.create(
            name="Rabies Vaccine",
            description="Used to prevent rabies in animals",
            manufacturer="VetPharma"
        )

    def test_vaccine_creation(self):
        self.assertEqual(self.vaccine.name, "Rabies Vaccine")
        self.assertEqual(self.vaccine.manufacturer, "VetPharma")
        self.assertIsNotNone(self.vaccine.created_at)


class AnimalVaccineRecordModelTest(TestCase):
    def setUp(self):
        # Create a Company for Animal
        self.company = Company.objects.create(name="Test Company")
        
        # Create an Animal linked to the Company
        self.animal = Animal.objects.create(
            eartag="12345",
            company=self.company,
            room="Room A",
            gender=True
        )
        
        # Create a Vaccine
        self.vaccine = Vaccine.objects.create(
            name="Rabies Vaccine"
        )
        
        # Create an Animal Vaccine Record
        self.record = AnimalVaccineRecord.objects.create(
            animal=self.animal,
            vaccine=self.vaccine,
            administered_by="Dr. Smith"
        )

    def test_animal_vaccine_record_creation(self):
        self.assertEqual(self.record.animal, self.animal)
        self.assertEqual(self.record.vaccine, self.vaccine)
        self.assertEqual(self.record.administered_by, "Dr. Smith")
        self.assertIsNotNone(self.record.date_administered)


class VaccineAPITest(APITestCase):
    def setUp(self):
        self.vaccine_data = {
            "name": "Rabies Vaccine",
            "description": "Used to prevent rabies in animals",
            "manufacturer": "VetPharma"
        }

    def test_create_vaccine(self):
        response = self.client.post('/api/vaccines/', self.vaccine_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Rabies Vaccine")

    def test_list_vaccines(self):
        Vaccine.objects.create(**self.vaccine_data)
        response = self.client.get('/api/vaccines/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class AnimalVaccineRecordAPITest(APITestCase):
    def setUp(self):
        # Create a Company for Animal
        self.company = Company.objects.create(name="Test Company")
        
        # Create an Animal linked to the Company
        self.animal = Animal.objects.create(
            eartag="12345",
            company=self.company,
            room="Room A",
            gender=True
        )
        
        # Create a Vaccine
        self.vaccine = Vaccine.objects.create(
            name="Rabies Vaccine"
        )
        
        # Animal Vaccine Record Data
        self.record_data = {
            "animal": self.animal.id,
            "vaccine": self.vaccine.id,
            "administered_by": "Dr. Smith",
        }

    def test_create_animal_vaccine_record(self):
        response = self.client.post('/api/vaccine-records/', self.record_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['administered_by'], "Dr. Smith")

    def test_list_animal_vaccine_records(self):
        AnimalVaccineRecord.objects.create(
            animal=self.animal,
            vaccine=self.vaccine,
            administered_by="Dr. Smith"
        )
        response = self.client.get('/api/vaccine-records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
