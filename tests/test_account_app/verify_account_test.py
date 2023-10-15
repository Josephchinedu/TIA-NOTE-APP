import json

from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import OTP, User
from tests.test_account_app.signup_test import CreateAccountApiViewTests


class VerifyAccountApiViewTests(APITestCase):
    def test_verify_otps(self, create_account=True):
        if create_account:
            CreateAccountApiViewTests.test_create_account(self)
        else:
            pass

        get_last_otp = OTP.objects.last()

        url = reverse("account:verify")

        data = {
            "email": "test@example.com",
            "otp": get_last_otp.code,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.json().get("error"), False)

    def test_invalid_otp(self):
        CreateAccountApiViewTests.test_create_account(self)

        url = reverse("account:verify")

        data = {
            "email": "test@example.com",
            "otp": ".code",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.json().get("message"), "invalid OTP.")
