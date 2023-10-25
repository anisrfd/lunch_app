from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from restaurant_app.models import Restaurant, Menu
from restaurant_app.serializers import MenuSerializer


class MenuUploadAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.url = f'/restaurant/{self.restaurant.id}/menu/upload/'

    def test_menu_upload_with_valid_data(self):
        data = {
            'restaurant': self.restaurant.id,
            'date': '2023-10-26',
            'items': 'Item 1, Item 2, Item 3'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Menu.objects.filter(restaurant=self.restaurant.id).exists())

    def test_menu_upload_invalid_data(self):
        data = {
            'restaurant': '',
            'date': '',
            'items': ''
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_menu_upload_missing_data(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
