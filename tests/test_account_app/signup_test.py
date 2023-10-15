import json

from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User


class CreateAccountApiViewTests(APITestCase):
    @patch("main.helpers.emails_helper.EmailHandler.signup_otp_confirmation")
    def test_create_account(self, mock_signup_otp_confirmation):
        url = reverse("account:signup")

        data = {
            "first_name": "test",
            "last_name": "user",
            "email": "test@example.com",
            "password": "iFiyU83h2sdxMdb/$.",
            "confirm_password": "iFiyU83h2sdxMdb/$.",
        }

        mock_signup_otp_confirmation.retrun_value = True
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_password_strength(self):
        url = reverse("account:signup")

        data = {
            "first_name": "test",
            "last_name": "user",
            "email": "test@example.com",
            "password": "testuser",
            "confirm_password": "testuser",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            response.json().get("non_field_errors")[0],
            "Password must contain at least one numeric digit",
        )

    def test_duplicate_email(self):
        User.objects.create_user(
            first_name="existing",
            last_name="user",
            email="test@example.com",
            password="existinguser",
        )

        url = reverse("account:signup")

        data = {
            "first_name": "test",
            "last_name": "user",
            "email": "test@example.com",
            "password": "iFiyU83h2sdxMdb/$.",
            "confirm_password": "iFiyU83h2sdxMdb/$.",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json().get("message"),
            "Email already exists",
        )
        self.assertEqual(User.objects.count(), 1)
