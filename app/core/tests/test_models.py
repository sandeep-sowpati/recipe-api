"""
test  for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models"""
    def test_create_user_with_email_successful(self):
        """Model to test creating user is working fine or not"""
        password = 'testpass123'
        email = 'test@example.com'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
