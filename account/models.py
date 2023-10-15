import random
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from account.managers import BaseModel, OTPManager, UserManager
from main.helpers.emails_helper import EmailHandler


# Create your models here.
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user profile.
    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "USER PROFILE"
        verbose_name_plural = "USER PROFILES"

    def __str__(self) -> str:
        return self.email

    def get_fullname(self) -> str:
        """
        Returns the full name of the person.
        If both the first name and last name are available,
        it concatenates them with a space in between and returns the full name.
        If either the first name or last name is missing, it returns None.
        Returns:
            str: The full name of the person, or None if first name or last name is missing.
        """
        if not self.first_name or not self.last_name:
            return None
        else:
            return f"{self.first_name} {self.last_name}"

    @classmethod
    def sign_up(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ) -> bool:
        """
        Validates and creates a new user instance.
        Args:
            cls (class): The class reference for the user model.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email address of the user.
            phone_number (str): The phone number of the user.
            password (str): The password for the user.
            is_investor (bool): Optional. Whether the user is an investor. Default is False.
            is_account_manager (bool): Optional. Whether the user is an account manager. Default is False.
        Returns:
            bool: True if the user instance is created successfully.
        """
        # format_dob = date_of_birth.strip()
        # date_of_birth = date(int(format_dob[0], int(format_dob[1]), int(format_dob[2])))

        user = cls.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_active=False,
        )
        otp = OTP.get_otp(
            type="REGISTRATION", recipient=user.email, length=6, expiry_time=10
        )

        # send_email = email_sender

        EmailHandler(email=user.email).signup_otp_confirmation(
            otp=otp.code, first_name=user.first_name, year=datetime.now().year
        )

        return user

    @classmethod
    def verify_user(cls, recipient: str, otp: str) -> dict:
        """
        Verifies the user profile based on the provided OTP.
        Args:
            cls (class): The class reference for the user model.
            recipient (str): The email address of the user profile to verify.
            otp (str): The one-time password to validate.
        Returns:
            dict: A dictionary containing the verification status and message.
        """
        verify = OTP.verify_otp(recipient=recipient, otp=otp)
        print("verify", verify)
        if verify.get("status") == True:
            user = cls.objects.filter(email=recipient)
            if user.exists():
                user.update(is_active=True)
                return {
                    "status": True,
                    "message": "USER PROFILE was verified successfully.",
                }
            return {
                "status": False,
                "message": "email is not registered to any USER PROFILE.",
            }
        return {"status": False, "message": verify.get("message")}

    @classmethod
    def resend_verification_code(cls, recipient: str) -> dict:
        """
        Resends the verification code to the provided email address.
        Args:
            cls (class): The class reference for the user model.
            recipient (str): The email address of the recipient.
        Returns:
            dict: A dictionary containing the status and message of the operation.
                - status (bool): True if the email was sent successfully, False otherwise.
                - message (str): Message describing the outcome of the operation.
        """

        # old otp
        otp_instance = OTP.objects.filter(recipient=recipient).last()
        if otp_instance:
            # time difference, check if it's more than 5 minutes
            time_difference = (
                datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
                - otp_instance.created_at
            )
            if time_difference.seconds < 300:
                return {
                    "status": False,
                    "message": "Please wait for 5 minutes before requesting for another OTP.",
                }

            otp_instance.delete()

        otp = OTP.get_otp(
            type="REGISTRATION", recipient=recipient, length=6, expiry_time=10
        )

        try:
            user_instance = cls.objects.get(email=recipient)
        except cls.DoesNotExist:
            return {"status": False, "message": "USER does not exist."}

        EmailHandler(email=recipient).signup_otp_confirmation(
            otp=otp.code, first_name=user_instance.first_name, year=datetime.now().year
        )

        return {"status": True, "message": "OTP sent successfully."}

    @classmethod
    def sign_in(cls, email: str, password: str) -> dict or None:
        """
        Authenticates a user with the provided email and password, generating a token for successful sign-in.
        Args:
            cls (class): The class reference for the user model.
            email (str): The email address of the user.
            password (str): The password of the user.
        Returns:
            dict or None: A dictionary containing sign-in information if successful, or None if authentication fails.
                - status (bool): The status of the sign-in attempt (True for success, False otherwise).
                - user (int): The ID of the authenticated user.
                - access (str): The access token for the authenticated user.
                - message (str): (Optional) A message indicating that the user profile is not verified.
        """

        from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
        from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

        user = authenticate(email=email, password=password)

        if user is not None:
            if not user.is_active:
                data = {
                    "error": True,
                    "message": "USER PROFILE is not active, please verify your account.",
                }
                return data

            tokenr = TokenObtainPairSerializer().get_token(user)
            access = AccessToken().for_user(user)

            user.last_login = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
            user.save()

            return {
                "error": False,
                "tokens": {
                    "refresh": str(tokenr),
                    "access": str(access),
                },
            }

            return data
        return None

    @classmethod
    def get_details(cls, id: str) -> object:
        """
        Retrieve user details based on the given ID.
        Args:
            cls (class): The class reference for the user model.
            id (str): The ID of the user to retrieve.
        Returns:
            object: The user object representing the details.
        Raises:
            Http404: If the user with the given ID does not exist.
        """
        try:
            user = cls.objects.get(id=id)
        except cls.DoesNotExist:
            return {"message": "user does not exist.", "status": False}
        return user

    @classmethod
    def change_password(
        cls, user: isinstance, old_password: str, new_password: str
    ) -> dict:
        """
        Change the password of a user.
        Args:
            cls (class): The class reference for the user model.
            user (object): The user object for which the password will be changed.
            old_password (str): The old password entered by the user.
            new_password (str): The new password to be set for the user.
        Returns:
            dict: A dictionary containing a message indicating the status of the password change.
        """
        if user:
            verify_password = check_password(old_password, user.password)
            if verify_password:
                # crosscheck passwords for similarities
                if old_password == new_password:
                    return {
                        "status": False,
                        "message": "similar password, try a new one.",
                    }
                user.set_password(new_password)
                user.save()
                return {"status": True, "message": "password changed successfully."}
            return {
                "status": False,
                "message": "old password is incorrect, forgot password?",
            }
        return {"status": False, "message": "user does not exist."}

    @classmethod
    def forgot_password(cls, email: str = None) -> dict:
        """
        Send a password reset OTP to the user's email or phone number.
        Args:
            email (str): User's email address for password reset. Defaults to None.
            phone_number (str): User's phone number for password reset. Defaults to None.
        Returns:
            dict: A dictionary containing the status and message of the operation.
                - status (bool): True if OTP sent successfully, False otherwise.
                - message (str): Message describing the outcome of the operation.
        """
        if email is not None:
            user = cls.objects.filter(email=email).first()
            if user is not None:
                otp = OTP.get_otp(
                    type="PASSWORD RESET", recipient=email, length=6, expiry_time=10
                )

                # send email
                EmailHandler(email=user.email).account_reset_request(
                    otp=otp.code, first_name=user.first_name, year=datetime.now().year
                )

                return {"status": True, "message": "OTP sent successfully."}

            return {"status": False, "message": "USER does not exist."}

        return {"status": False, "message": "invalid or expired OTP."}

    @classmethod
    def reset_password(
        cls,
        otp: str,
        new_password: str,
        email: str = None,
    ):
        """
        Set a new password for an existing user.
        Args:
            cls (class): The class reference for the user model.
            otp (str): One time password used for verification.
            new_password (str): The new password to be set for the user.
            email (str): User's email address for password reset. Defaults to None.
            phone_number (str): User's phone number for password reset. Defaults to None.
        Returns:
            dict: A dictionary containing the status and message of the operation.
                - status (bool): True if password reset was successful, False otherwise.
                - message (str): Message describing the outcome of the operation.
        """
        verify = OTP.verify_otp(recipient=email, otp=otp)
        if verify.get("status") == True:
            if email is not None:
                user = cls.objects.filter(email=email).first()
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    return {"status": True, "message": "password reset was successful."}
                return {"status": False, "message": "USER PROFILE does not exist."}

        return {"status": False, "message": verify.get("message")}

    @classmethod
    def update_user_details(
        cls,
        user,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        address: str = None,
    ):
        """
        Update the details of a user object based on the provided parameters.
        Args:
            cls (class): The class reference for the user model.
            user (User): The User object.
            first_name (str): The new first name of the user.
            middle_name (str): The new middle name of the user.
            last_name (str): The new last name of the user.
            address (str): The new address of the user.
        Returns:
            user: If the user is found and updated successfully, returns the updated user object.
            None: If the user is not found or inactive, returns None.
        """
        user = cls.objects.filter(email=user.email, is_active=True).first()
        if user is not None:
            user.first_name = first_name if first_name is not None else user.first_name
            user.middle_name = (
                middle_name if middle_name is not None else user.middle_name
            )
            user.last_name = last_name if last_name is not None else user.last_name
            user.address = address if address is not None else user.address
            user.save()
            return user
        return None


class OTP(BaseModel):
    """
    Model representing a One-Time Password (OTP).
    Attributes:
        type (str): The type of the OTP (e.g., "registration", "password-reset", etc.).
        recipient (str): The recipient's identifier (e.g., email address, phone number).
        length (int): The length of the OTP code.
        expiry_time (int): The validity period of the OTP in seconds.
        code (str): The generated OTP code.
        is_used (bool): Flag indicating whether the OTP has been used or not.
    Relationships:
        objects (OTPManager): Custom manager for OTP objects.
    """

    type = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    length = models.IntegerField()
    expiry_time = models.IntegerField()
    code = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)

    objects = OTPManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "ONE TIME PASSWORD"
        verbose_name_plural = "ONE TIME PASSWORDS"

    def __str__(self) -> str:
        return self.recipient

    @property
    def time_valid(self):
        """
        Property that checks if the object's created time is still within the valid time range.
        Returns:
            bool: True if the object's created time is within the valid time range, False otherwise.
        """
        current_time = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        return (
            True
            if self.created_at > current_time - timedelta(minutes=self.expiry_time)
            else False
        )
        # return True

    @classmethod
    def get_otp(cls, type: str, recipient: str, length: int = 6, expiry_time: int = 5):
        """
        Generate and retrieve a new OTP (One-Time Password) object.
        Args:
            type (str): The type of the OTP.
            recipient (str): The recipient of the OTP.
            length (int, optional): The length of the OTP. Defaults to 6.
            expiry_time (int, optional): The expiry time of the OTP in minutes. Defaults to 5.
        Returns:
            OTP: The newly created OTP object.
        """
        # generate random otp code
        code = "".join([str(random.randint(0, 9)) for _ in range(length)])

        otp = cls.objects.create(
            type=type,
            recipient=recipient,
            length=length,
            expiry_time=expiry_time,
            code=code,
        )
        return otp

    @classmethod
    def verify_otp(cls, recipient: str, otp: str) -> dict:
        """
        Verify the OTP (One-Time Password) for the given recipient.
        Args:
            recipient (str): The recipient for whom to verify the OTP.
            otp (str): The OTP to be verified.
        Returns:
            dict: A dictionary containing the verification status and message.
                - If the OTP is valid and not expired, the status will be True and the message will be "OTP is valid for recipient."
                - If the OTP is invalid or expired, the status will be False and the message will be "invalid or expired OTP."
                - If no valid OTP is found for the recipient, the status will be False and the message will be "invalid or expired OTP."
        """
        one_time_password = cls.objects.filter(
            recipient=recipient, is_used=False
        ).first()

        if one_time_password is not None:
            if one_time_password.time_valid:
                verified = otp == one_time_password.code
                if verified:
                    one_time_password.is_used = True
                    one_time_password.save()
                    return {"status": True, "message": "OTP is valid for recipient."}
                return {"status": False, "message": "invalid OTP."}
            return {"status": False, "message": "expired OTP."}
        return {"status": False, "message": "invalid OTP."}
