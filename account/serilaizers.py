from rest_framework import serializers

from account.models import User
from main.helpers.reusable import validate_password


class CreateAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        if len(attrs.get("password")) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")

        val, msg = validate_password(attrs.get("password"))

        if val == False:
            raise serializers.ValidationError(msg)

        return attrs


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=255)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        if len(attrs.get("new_password")) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")

        val, msg = validate_password(attrs.get("new_password"))

        if val == False:
            raise serializers.ValidationError(msg)

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)


class AccountResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        if len(attrs.get("password")) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")

        val, msg = validate_password(attrs.get("password"))

        if val == False:
            raise serializers.ValidationError(msg)

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "created_at",
            "updated_at",
            "last_login",
        ]
