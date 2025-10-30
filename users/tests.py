from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('users-list-create')
        data = {"nombre": "Test", "email": "test@example.com", "telefono": "1234"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_list_users(self):
        User.objects.create(nombre="Ana", email="ana@demo.com", telefono="4567")
        url = reverse('users-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
