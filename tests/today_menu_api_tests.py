from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from datetime import date
from restaurant_app.models import Menu, Restaurant
from restaurant_app.serializers import MenuSerializer


class TodayMenuAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.today_date = date.today()
        self.menu_today = Menu.objects.create(restaurant=self.restaurant, date=self.today_date, items='Menu for today')
        self.menu_other_date = Menu.objects.create(restaurant=self.restaurant, date=date(2023, 1, 1),
                                                   items='Menu for another date')
        self.url = '/menu/today/'

    def test_today_menu(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Menu for today', str(response.data))

    def test_today_menu_no_menus(self):
        self.menu_today.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_today_menu_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
