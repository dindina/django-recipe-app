from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer
from decimal import Decimal


RECIPES_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    """Create a test receipe"""

    defaults = {
        "title": "Sample title",
        "time_minutes": 2,
        "price": Decimal("3.1"),
        "description": "sample desc",
    }

    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):

        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, 401)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "yse@example.com", "testpasswwe"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_recipes_for_authenticated_user(self):

        one_more_user = get_user_model().objects.create_user(
            "test1@example.com", "testpass111"
        )

        create_recipe(user=self.user)
        create_recipe(user=one_more_user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, 200)
