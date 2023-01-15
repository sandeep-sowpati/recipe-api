"""
Test from user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

TOKEN_URL = reverse('user:token')

ME_URL = reverse('user:about')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class publicUserApiTests(TestCase):
    """Test the public features of user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a successful user"""
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'test user'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists(self):
        """Test to check if the user email already exists or not"""
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'test user'
        }

        create_user(**payload)

        payload2 = {
            'email': 'test@example.com',
            'password': 'Hello',
            'name': 'Hello'
        }
        res = self.client.post(CREATE_USER_URL, payload2)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test to check if password is less than 5 chars and throw an error"""
        payload = {
            'email': 'test@example.com',
            'password': 'hell',
            'name': 'sand',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test for bad credentials"""
        create_user(email='test@example.com', password='Hell123')

        pay_load = {
            'email': 'test@example.com',
            'password': 'HEll123',
        }
        res = self.client.post(TOKEN_URL, pay_load)

        self.assertNotIn('token', res)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_for_blank_passwords(self):
        """Test for blank passsword"""
        pay_load = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, pay_load)

        self.assertNotIn('token', res)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_profile_unauthorized(self):
        """Test to retrieve profile if not authorized"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class privateUserApiTests(TestCase):
    """Test API that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='pass123',
            name='Test User',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test to check if we are able to retrieve a profile successfully. """
        res = self.client.get(ME_URL)

        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the end point."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for the authenticated user"""
        payload = {'name': 'updated_name', 'password': 'newpassword'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
