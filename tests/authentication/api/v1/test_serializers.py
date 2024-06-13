from rest_framework.serializers import ErrorDetail
from rest_framework.test import APITestCase

from sigma.authentication.api.v1.serializers import RegisterUserSerializer
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
