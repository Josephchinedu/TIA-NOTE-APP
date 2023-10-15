import json

from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import OTP, User
from tests.test_account_app.signup_test import CreateAccountApiViewTests
from tests.test_account_app.verify_account_test import VerifyAccountApiViewTests


class ChagePasswordApiViewTests(APITestCase):
    def test_similat_password_onchange_password_for_authenticated_user(self):
        CreateAccountApiViewTests.test_create_account(self)

        # user
        User.objects.all().update(is_active=True)

        url = reverse("account:login")

        data = {
            "email": "test@example.com",
            "password": "iFiyU83h2sdxMdb/$.",
        }

        login_response = self.client.post(url, data, format="json")

        url = reverse("account:change_password")

        data = {
            "old_password": "iFiyU83h2sdxMdb/$.",
            "new_password": "iFiyU83h2sdxMdb/$.",
            "confirm_password": "iFiyU83h2sdxMdb/$.",
        }

        headers = {
            "Authorization": f"Bearer {login_response.json()[0].get('tokens', {}).get('access')}"
        }

        response = self.client.post(url, data, headers=headers, format="json")

        self.assertEqual(
            response.json().get("message"), "similar password, try a new one."
        )

    def test_change_password_for_authenticated_user(self):
        CreateAccountApiViewTests.test_create_account(self)

        # user
        User.objects.all().update(is_active=True)

        url = reverse("account:login")

        data = {
            "email": "test@example.com",
            "password": "iFiyU83h2sdxMdb/$.",
        }

        login_response = self.client.post(url, data, format="json")

        url = reverse("account:change_password")

        data = {
            "old_password": "iFiyU83h2sdxMdb/$.",
            "new_password": "iFiyU83h2sdxMdb/$./",
            "confirm_password": "iFiyU83h2sdxMdb/$./",
        }

        headers = {
            "Authorization": f"Bearer {login_response.json()[0].get('tokens', {}).get('access')}"
        }

        response = self.client.post(url, data, headers=headers, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get("message"), "password changed successfully."
        )
