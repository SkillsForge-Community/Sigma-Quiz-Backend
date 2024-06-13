from unittest.mock import MagicMock

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ErrorDetail
from rest_framework.test import APITestCase

from sigma.authentication.api.v1.serializers import (
    ChangePasswordSerializer,
    LogInSerializer,
    RegisterUserSerializer,
)
from tests.authentication.factories import User, UserModelFactory


class RegisterUserSerializerTests(APITestCase):

    def test_error_raised_for_invalid_length_of_password(self):
        """Test error raised for invalid length of password"""

        request_data = {
            "first_name": "mimi",
            "last_name": "jose",
            "email": "mimijose@mail.com",
            "roles": ["super-admin"],
            "password": "123",
        }

        serializer = RegisterUserSerializer(data=request_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["password"],
            [
                ErrorDetail(
                    string="Password must be minimum of eight(8) characters", code="Short Password"
                )
            ],
        )

    def test_error_raised_for_creation_of_account_with_an_existing_email(self):
        """Test error raised for creation of account with an existing email"""
        UserModelFactory(email="delight@mail.com")

        request_data = {
            "first_name": "mimi",
            "last_name": "jose",
            "email": "delight@mail.com",
            "roles": ["super-admin"],
            "password": "12345628282",
        }

        serializer = RegisterUserSerializer(data=request_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["email"],
            [
                ErrorDetail(
                    string=f"Key (email)=({request_data['email']}) already exists.",
                    code="Bad Request",
                )
            ],
        )

    def test_creation_of_account_with_valid_data(self):
        """Test creation of account with valid data"""

        request_data = {
            "first_name": "mimi",
            "last_name": "jose",
            "email": "mimijose@mail.com",
            "roles": ["super-admin"],
            "password": "12345628282",
        }

        serializer = RegisterUserSerializer(data=request_data)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertIsNotNone(User.objects.filter(email=request_data["email"]).first())


class TestSignInSerializer(APITestCase):

    def test_valid_data(self):
        """Test serializer with valid data"""
        user = UserModelFactory(email="john@mail.com", password="123456789")
        user.set_password(user.password)
        user.save()

        data = {"email": user.email, "password": "123456789"}
        serializer = LogInSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIn("access_token", serializer.data)
        self.assertIn("user", serializer.data)

    def test_missing_email(self):
        """Test serializer with missing email"""

        serializer = LogInSerializer(data={"password": "123456789"})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("email", context.exception.detail)

    def test_missing_password(self):
        """Test serializer with missing password"""

        serializer = LogInSerializer(data={"email": "john@mail.com"})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("password", context.exception.detail)

    def test_invalid_email(self):
        """Test serializer with invalid email"""
        data = {"email": "invalid_email", "password": "123456789"}
        serializer = LogInSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("email", context.exception.detail)


class ChangePasswordSerializerTests(APITestCase):

    def setUp(self):
        self.user = UserModelFactory(email="delight@mail.com")
        self.user.set_password("old_password")
        self.user.save()

    def test_error_raised_for_short_length_of_password(self):
        """Test error raised for short length of password"""

        request = MagicMock()
        request.user = self.user

        data = {"old_password": "old_password", "new_password": "new"}
        serializer = ChangePasswordSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["new_password"][0],
            ErrorDetail(
                string="Password must be minimum of eight(8) characters", code="Short Password"
            ),
        )

    def test_error_not_raised_when_when_valid_data_are_provided(self):
        """Test user password changed when valid data are provided"""

        request = MagicMock()
        request.user = self.user

        data = {"old_password": "old_password", "new_password": "new_password"}

        serializer = ChangePasswordSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid())
