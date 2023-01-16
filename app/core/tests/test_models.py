"""
test  for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from decimal import Decimal

from core import models


class USerModelTests(TestCase):
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

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'test2@example.com'],
            ['Test3@EXAMPLE.COm', 'test3@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_wo_email_raises_error(self):
        """Test that creating a user without an email raise a valueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class RecipeModelTests(TestCase):
    """Test to check if recipe model is working or not."""
    def test_create_recipe(self):
        """Test to check functionality of create recipe api"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe Name',
            time_in_minutes=5,
            price=Decimal('205.50'),
            description="Sample recipe Description",
        )

        self.assertEqual(str(recipe), recipe.title)
