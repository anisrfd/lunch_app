from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from restaurant_app.views import register


class RegistrationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/register/'

    def test_user_registration_with_valid_data(self):
        user_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_missing_fields(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username='testuser').exists())
