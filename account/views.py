from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, status
from rest_framework.decorators import authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from account.models import User
from account.serilaizers import (
    AccountResetSerializer,
    ChangePasswordSerializer,
    CreateAccountSerializer,
    EmailSerializer,
    LoginSerializer,
    VerifyAccountSerializer,
)


class CreateAccountApiView(APIView):
    """
    CREATE ACCOUNT API VIEW

    BODY PARAMS:
    {
        "first_name": "test",
        "last_name": "user",
        "email": "",
        "password": "testuser",
        "confirm_password": "testuser"
    }
    """

    # initialize serializer class
    serializer_class = CreateAccountSerializer

    # swagger schema
    create_user_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "confirm_password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["username", "email", "password", "confirm_password"],
    )

    create_user_response_schema = {
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "tokens": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    }
    # end swagger schema

    # csrf exempt for cross origin request
    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["authentications"],
        request_body=create_user_schema,
        responses=create_user_response_schema,
    )
    def post(self, request):
        """
        THIS METHOD ACCEPT POST REQUEST AND CREATE USER ACCOUNT
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  # raise exception if validation fails

        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        password = serializer.validated_data.get("password")
        email = serializer.validated_data.get("email")

        try:
            User.objects.get(email=email)
            return Response(
                {"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            pass

        User.sign_up(
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )

        return Response(
            {
                "message": "Account created successfully, an activation code has been sent to your email"
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyAccountApiView(APIView):
    """
    VERIFY ACCOUNT API VIEW

    BODY PARAMS:
    {
        "email": "",
        "otp": ""
    }


    """

    # initialize serializer class
    serializer_class = VerifyAccountSerializer

    # swagger schema
    verify_user_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
            "otp": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["email", "otp"],
    )

    verify_user_response_schema = {
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "tokens": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    }

    # end swagger schema

    # csrf exempt for cross origin request
    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["authentications"],
        request_body=verify_user_schema,
        responses=verify_user_response_schema,
    )
    def post(self, request):
        """
        THIS METHOD ACCEPT POST REQUEST AND VERIFY USER ACCOUNT

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")

        verify_user = User.verify_user(recipient=email, otp=otp)
        if verify_user.get("status") == False:
            return Response(
                {"message": verify_user.get("message")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)

        tokenr = TokenObtainPairSerializer().get_token(user)
        access = AccessToken().for_user(user)

        return Response(
            {
                "error": False,
                "code": "HTTP_200_OK",
                "tokens": {
                    "refresh": str(tokenr),
                    "access": str(access),
                },
            },
            status=status.HTTP_200_OK,
        )


class ResendActivationCode(APIView):
    """
    RESEND ACTIVATION CODE API VIEW

    BODY PARAMS:
    {
        "email": ""
    }
    """

    serializer_class = EmailSerializer

    resend_activation_code_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
        },
        required=["email"],
    )

    resend_activation_code_response_schema = {
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["authentications"],
        request_body=resend_activation_code_schema,
        responses=resend_activation_code_response_schema,
    )
    def post(self, request):
        """
        THIS METHOD ACCEPT POST REQUEST AND RESEND ACTIVATION CODE
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        resend_otp_code = User.resend_verification_code(recipient=email)
        if resend_otp_code.get("status") == False:
            return Response(
                {"message": resend_otp_code.get("message")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": resend_otp_code.get("message")},
            status=status.HTTP_200_OK,
        )


class ChangePasswordApiView(APIView):
    """
    This class handles change password
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ChangePasswordSerializer

    change_password_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "old_password": openapi.Schema(type=openapi.TYPE_STRING),
            "new_password": openapi.Schema(type=openapi.TYPE_STRING),
            "confirm_password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["old_password", "new_password", "confirm_password"],
    )

    change_password_response_schema = {
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["authentications"],
        request_body=change_password_schema,
        responses=change_password_response_schema,
    )
    def post(self, request):
        """
        This method accepts post request and change password
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        user = request.user

        change_password_status = User.change_password(
            user=user, old_password=old_password, new_password=new_password
        )
        if change_password_status.get("status") == False:
            return Response(
                {"message": change_password_status.get("message")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": change_password_status.get("message")},
            status=status.HTTP_200_OK,
        )


class LoginApiView(APIView):
    """
    LOGIN API VIEW

    """

    serializer_class = LoginSerializer

    login_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["email", "password"],
    )

    login_response_schema = {
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "tokens": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["authentications"],
        request_body=login_schema,
        responses=login_response_schema,
    )
    def post(self, request):
        """
        THIS METHOD ACCEPT POST REQUEST AND LOGIN USER
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        login_data = User.sign_in(email=email, password=password)
        if login_data is None:
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # print("login_data", login_data)

        if login_data.get("error") == True:
            return Response(
                {"message": login_data.get("message")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = (
            {
                "error": False,
                "code": "HTTP_200_OK",
                "tokens": {
                    "refresh": login_data.get("tokens", {}).get("refresh"),
                    "access": login_data.get("tokens", {}).get("access"),
                },
            },
        )

        return Response(data, status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    """
    FORGOT PASSWORD API VIEW
    """

    serializer_class = EmailSerializer

    forgot_password_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
        },
        required=["email"],
    )

    forgot_password_response_schema = {
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["authentications"],
        request_body=forgot_password_schema,
        responses=forgot_password_response_schema,
    )
    def post(self, request):
        """
        THIS METHOD ACCEPT POST REQUEST AND SEND FORGOT PASSWORD EMAIL
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        forgot_password = User.forgot_password(email=email)
        if forgot_password.get("status") == False:
            return Response(
                {"message": forgot_password.get("message")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": forgot_password.get("message")},
            status=status.HTTP_200_OK,
        )


class AccountResetApiView(APIView):
    """
    ACCOUNT RESET API VIEW
    """

    serializer_class = AccountResetSerializer

    account_reset_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
            "otp": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "confirm_password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["email", "otp", "password", "confirm_password"],
    )

    account_reset_response_schema = {
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["authentications"],
        request_body=account_reset_schema,
        responses=account_reset_response_schema,
    )
    def post(self, request):
        """
        THIS METHOD ACCEPT POST REQUEST AND RESET USER PASSWORD
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")
        password = serializer.validated_data.get("password")

        account_reset = User.reset_password(email=email, otp=otp, new_password=password)
        if account_reset.get("status") == False:
            return Response(
                {"message": account_reset.get("message")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": account_reset.get("message")},
            status=status.HTTP_200_OK,
        )
