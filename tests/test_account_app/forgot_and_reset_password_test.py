from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import OTP, User
from tests.test_account_app.signup_test import CreateAccountApiViewTests


class ForgotPasswordTests(APITestCase):
    @patch("main.helpers.emails_helper.EmailHandler.signup_otp_confirmation")
    def test_forgot_password_valid_email(self, mock_signup_otp_confirmation):
        mock_signup_otp_confirmation.retrun_value = True

        CreateAccountApiViewTests.test_create_account(self)

        url = reverse("account:forgot_password")

        payload = {"email": "test@example.com"}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "OTP sent successfully.")

    def test_forgot_password_invalid_email(self):
        url = reverse("account:forgot_password")

        payload = {"email": "ffff@aby.com"}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("message"), "USER does not exist.")

    def test_verify_otp_and_reset_password(self):
        CreateAccountApiViewTests.test_create_account(self)
        email = "test@example.com"

        otp_instance = OTP.objects.filter(recipient=email).last()

        url = reverse("account:reset_password")

        payload = {
            "email": email,
            "otp": otp_instance.code,
            "password": "iFiyU83h2sdxMdb/$.2233",
            "confirm_password": "iFiyU83h2sdxMdb/$.2233",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get("message"), "password reset was successful."
        )

    def test_verify_otp_and_reset_password_invalid_otp(self):
        CreateAccountApiViewTests.test_create_account(self)
        email = "test@example.com"

        # otp_instance = OTP.objects.last(recipient=email)

        url = reverse("account:reset_password")

        payload = {
            "email": email,
            "otp": "1234",
            "password": "iFiyU83h2sdxMdb/$.2233",
            "confirm_password": "iFiyU83h2sdxMdb/$.2233",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("message"), "invalid OTP.")
