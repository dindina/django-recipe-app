"""
Test for the user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):

    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_sucess(self):
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "name": "Dinesh",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, 201)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_exists_error(self):

        payload = {
            "email": "test@example.com",
            "password": "test123",
            "name": "Dinesh",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, 400)

    def test_password_too_short_error(self):

        payload = {
            "email": "test@example.com",
            "password": "te",
            "name": "Dinesh",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, 400)
        user_objects = get_user_model().objects.filter(email=payload["email"])
        user_exists = user_objects.exists()
        self.assertFalse(user_exists)


def test_create_token_for_user(self):

    user_details = {
        "email": "test@example.com",
        "password": "te",
        "name": "Dinesh",
    }
    create_user(**user_details)

    payload = {
        "email": user_details["email"],
        "password": user_details["password"],
    }
    res = self.client.post(TOKEN_URL, payload)

    self.assertEquals(res.status_code, 200)
    self.assertIn("token", res.data)


def test_create_token_bad_credentials(self):

    user_details = {
        "email": "test@example.com",
        "password": "goodpass",
        "name": "Dinesh",
    }
    create_user(**user_details)

    payload = {
        "email": user_details["email"],
        "password": "badpassword",
    }
    res = self.client.post(TOKEN_URL, payload)

    self.assertEquals(res.status_code, 400)
    self.assertNotIn("token", res.data)


def test_retrieve_user_unuth(self):

    res = self.client.post(ME_URL)
    self.assertEquals(res.status_code, 401)


class PrivateUserApiTest(TestCase):

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="teessss123",
            name="Dinesh",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):

        res = self.client.get(ME_URL)
        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            res.data,
            {
                "name": self.user.name,
                "email": self.user.email,
            },
        )

    def test_update_user_profile(self):

        payload = {
            "email": "test@example.com",
            "password": "updatedpassword123",
            "name": "Dinesh.R",
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertEqual(res.status_code, 200)
