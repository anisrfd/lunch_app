from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from restaurant_app.models import Menu, Restaurant, Employee, Vote


class GetWinnerAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.employee = Employee.objects.create(user=self.user)
        self.today_date = date.today()
        self.yesterday = self.today_date - timedelta(days=1)
        self.day_before_yesterday = self.today_date - timedelta(days=2)

        self.menu_today = Menu.objects.create(restaurant=self.restaurant, date=self.today_date, items='Menu for today')
        self.menu_yesterday = Menu.objects.create(restaurant=self.restaurant, date=self.yesterday,
                                                  items='Menu for yesterday')
        self.menu_day_before_yesterday = Menu.objects.create(restaurant=self.restaurant,
                                                             date=self.day_before_yesterday,
                                                             items='Menu for day before yesterday')
        self.url = '/menu/results/'

    def test_get_winner(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('winning_restaurant', response.data)

    def test_get_winner_no_previous_winner(self):
        # Delete the menus for the last two days to simulate no previous winner
        Menu.objects.filter(date=self.yesterday).delete()
        Menu.objects.filter(date=self.day_before_yesterday).delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('winning_restaurant', response.data)

    def test_get_winner_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
