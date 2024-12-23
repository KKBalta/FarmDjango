from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import RationComponent

class RationComponentTests(TestCase):
    def setUp(self):
        # Set up a test client
        self.client = APIClient()

        # Set up initial data for RationComponent
        self.ration_component_data = {
            'name': 'Test Component',
            'description': 'Test description for ration component',
            'dry_matter': 85.0,
            'calori': 12.5,
            'nisasta': 10.0,
            'price': 5.0
        }
        self.ration_component = RationComponent.objects.create(**self.ration_component_data)
        self.url = f'/api/ration-components/{self.ration_component.id}/'

    def test_get_ration_component(self):
        # Send GET request to retrieve a RationComponent
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.ration_component.name)
        self.assertEqual(response.data['description'], self.ration_component.description)

    def test_create_ration_component(self):
        # Send POST request to create a new RationComponent
        new_component_data = {
            'name': 'New Component',
            'description': 'Description for new component',
            'dry_matter': 90.0,
            'calori': 15.0,
            'nisasta': 8.0,
            'price': 4.5
        }
        response = self.client.post('/api/ration-components/', new_component_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_component_data['name'])
        self.assertEqual(response.data['description'], new_component_data['description'])

    def test_update_ration_component(self):
        # Send PUT request to update the existing RationComponent
        updated_data = {
            'name': 'Updated Component',
            'description': 'Updated description for ration component',
            'dry_matter': 88.0,
            'calori': 13.0,
            'nisasta': 9.0,
            'price': 6.0
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['description'], updated_data['description'])

    def test_delete_ration_component(self):
        # Send DELETE request to remove the RationComponent
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Confirm that the object is actually deleted
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
