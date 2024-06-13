import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from tests.authentication.factories import User, UserModelFactory


def format_time(time):
    """This format time to suite the desired time needed in the response body"""
    return (
        time.replace(tzinfo=datetime.timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


class RegisterAdminAPIViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("authentication:register_admin")

    def test_creation_of_user_with_valid_data(self):
        """Test creation of user with valid data"""

        request_data = {
            "first_name": "delight",
            "last_name": "jose",
            "email": "delightjose@mail.com",
            "password": "delightjoseph",
            "roles": ["super-admin"],
        }

        response = self.client.post(self.url, request_data, format="json")

        self.assertEqual(response.status_code, 201)

        user = User.objects.filter(email=request_data["email"]).first()

        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(request_data["password"]))

        self.assertEqual(
            response.json(),
            {
                "first_name": "delight",
                "last_name": "jose",
                "email": "delightjose@mail.com",
                "roles": ["super-admin"],
                "id": str(user.id),
                "created_at": format_time(user.created_at),
                "updated_at": format_time(user.updated_at),
            },
        )

    def test_account_not_created_with_invalid_data(self):
        """Test account not created with invalid data"""

        request_data = {
            "first_name": "delight",
            "last_name": "jose",
            "roles": ["super-admin"],
        }

        response = self.client.post(self.url, request_data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "error": "missing required field",
                "statusCode": 400,
                "message": "email is required",
            },
        )

        self.assertEqual(User.objects.count(), 0)

    def test_account_not_created_when_given_email_that_exists(self):
        """Test account not created when email exists"""
        UserModelFactory(email="delight@mail.com")

        request_data = {
            "first_name": "delight",
            "last_name": "jose",
            "roles": ["super-admin"],
            "email": "delight@mail.com",
            "password": "delightjose",
        }

        response = self.client.post(self.url, request_data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "error": "Bad Request",
                "statusCode": 400,
                "message": f"Key (email)=({request_data['email']}) already exists.",
            },
        )

        self.assertEqual(User.objects.filter(email=request_data["email"]).count(), 1)
