from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from tests.test_account_app.signup_test import CreateAccountApiViewTests
from tests.test_account_app.verify_account_test import VerifyAccountApiViewTests


class LoginApiViewTests(APITestCase):
    def test_login(self):
        CreateAccountApiViewTests.test_create_account(self)

        VerifyAccountApiViewTests.test_verify_otps(self, create_account=False)

        url = reverse("account:login")

        data = {
            "email": "test@example.com",
            "password": "iFiyU83h2sdxMdb/$.",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get("error"), False)

    def test_invalid_login(self):
        CreateAccountApiViewTests.test_create_account(self)

        url = reverse("account:login")

        data = {
            "email": "test@example.com",
            "password": "3h2sdxMdb/$.",
        }

        response = self.client.post(url, data, forma="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("message"), "Invalid email or password")


