"""
Test for models
"""

from decimal import Decimal


from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):

        email = "test@exampl.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalised(self):

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@Example.com", "TEST3@example.com"],
        ]

        for email, expected in sample_emails:

            user = get_user_model().objects.create_user(email, "samle123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):

        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user("", "samle123")
            return user

    def test_new_create_super_user(self):

        userobjects = get_user_model().objects
        user = userobjects.create_superuser("test@example.com", "samle123")

        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)

    def test_create_receipe(self):

        user = get_user_model().objects.create_user("teste2xample.com", "testpass1243")

        recipe = models.Recipe.objects.create(
            user=user,
            title="test receipe",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample reciper desc",
        )

        self.assertEqual(str(recipe), recipe.title)
