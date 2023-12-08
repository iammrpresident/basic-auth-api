from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

class AuthenticationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        # Test user data for registration
        self.valid_user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'Case',
        }

    def test_register_view(self):
        # Test registration with valid data
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

        # Test registration with existing email
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_view(self):
        # Register a user for login testing
        user = get_user_model().objects.create_user(**self.valid_user_data)

        # Test login with valid credentials
        login_credentials = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, login_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('Authorization', response.headers)

        # Test login with invalid credentials
        invalid_credentials = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


