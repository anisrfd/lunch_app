from datetime import date
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from restaurant_app.models import Menu, Restaurant, Employee, Vote
from restaurant_app.serializers import MenuSerializer


class VoteForMenuAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and obtain an authentication token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.employee = Employee.objects.create(user=self.user)
        self.today_date = date.today()
        self.menu_today = Menu.objects.create(restaurant=self.restaurant, date=self.today_date, items='Menu for today')
        self.url = f'/menu/{self.menu_today.id}/vote/'

    def test_vote_for_menu(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vote = Vote.objects.filter(menu=self.menu_today, employee=self.employee).first()
        self.assertIsNotNone(vote)

    def test_vote_for_nonexistent_menu(self):
        url = '/menu/999/vote/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vote_for_menu_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
