from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from restaurant_app.models import Restaurant
from restaurant_app.serializers import RestaurantSerializer


class RestaurantCreateAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = '/restaurant/create/'

    def test_create_restaurant_With_valid_data(self):
        data = {
            "name": "Test Restaurant",
        }

        response = self.client.post( self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Restaurant.objects.filter(name="Test Restaurant").exists())

    def test_create_restaurant_missing_data(self):
        response = self.client.post( self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Restaurant.objects.filter(name="Test Restaurant").exists())

    def test_create_restaurant_invalid_data(self):
        data = {
            "name": "",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
