import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def api_client():
    """Fixture for creating an instance of the Django test client."""
    return APIClient()


@pytest.fixture(scope="function")
def mock_user(db):
    """Fixture for creating a mock user for testing."""

    user = mixer.blend("users.User", roles=["super-admin"])
    print(
        f"First-Name: {user.first_name}\n"
        f"Last-Name: {user.last_name}\n"
        f"Email: {user.email}\n"
        f"Roles: {', '.join(user.roles)}"
    )

    yield user
    user.delete()


@pytest.mark.django_db
class TestUserListView:
    """
    Test View To List All Users
    """

    @pytest.fixture(autouse=True)
    def setup(self, api_client, mock_user):
        self.api_client = api_client
        self.mock_user = mock_user
        self.url = reverse("user-list")

    def test_list_users_unauthorized(self):
        """Test Unauthorized"""

        response = self.api_client.get(self.url)
        assert response.status_code == 401

    def test_list_users_authorized_super_admin(self):
        """Test Authorized as super-admin"""

        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.get(self.url)
        assert response.status_code == 200

    def test_list_users_forbidden_for_non_super_admin(self):
        """Test Authorized as non super-admin"""

        self.mock_user.roles = ["adhoc"]
        self.mock_user.save()
        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.get(self.url)
        assert response.status_code == 403


@pytest.mark.django_db
class TestUserProfileView:
    """
    Test View To Retrieve User Profile
    """

    @pytest.fixture(autouse=True)
    def setup(self, api_client, mock_user):
        self.api_client = api_client
        self.mock_user = mock_user
        self.url = reverse("user-profile")

    def test_user_profile_view_unauthorized(self):
        """Test retrieving the current user's profile un-authorized"""

        response = self.api_client.get(self.url)
        assert response.status_code == 401

    def test_user_profile_view_authorized(self):
        """Test retrieving the current user's profile authorized"""

        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.get(self.url)
        assert response.status_code == 200
        assert response.data["email"] == self.mock_user.email

    def test_user_profile_with_invalid_token(self):
        """Test profile retrieval with invalid token"""

        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
        response = self.api_client.get(self.url)
        assert response.status_code == 401

    def test_user_profile_with_different_roles(self):
        """Test profile retrieval for users with different roles"""

        # Test super-admin
        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == self.mock_user.email
        assert response.data["roles"] == ["super-admin"]

        # Test quiz-master
        self.mock_user.roles = ["quiz-master"]
        self.mock_user.save()
        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == self.mock_user.email
        assert response.data["roles"] == ["quiz-master"]


@pytest.mark.django_db
class TestUserRetrieveDestroyView:
    """
    Tests for retrieving and destroying a user account.
    """

    @pytest.fixture(autouse=True)
    def setup(self, api_client, mock_user):
        self.api_client = api_client
        self.mock_user = mock_user
        self.url = reverse(
            "user-retrieve-destroy",
            kwargs={"id": self.mock_user.id},
        )
        self.invalid_id_url = reverse(
            "user-retrieve-destroy",
            kwargs={"id": "308f5fc8-ff04-4c1d-bc6d-ea1dab4343c1"},
        )
        self.User = get_user_model()

    def test_retrieve_user_unauthorized(self):
        """Test unauthorized retrieval of user"""

        response = self.api_client.get(self.url)
        assert response.status_code == 401

    def test_delete_user_unauthorized(self):
        """Test unauthorized deletion of user"""

        response = self.api_client.delete(self.url)
        assert response.status_code == 401

    def test_retrieve_user_authorized(self):
        """Test authorized retrieval of user"""

        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == self.mock_user.email

    def test_delete_user_authorized(self):
        """Test authorized deletion of user"""

        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        user_exists = self.User.objects.filter(id=self.mock_user.id).exists()
        assert not user_exists

    def test_retrieve_user_with_invalid_id(self):
        """Test retrieval with an invalid user ID"""

        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.get(self.invalid_id_url)
        assert response.status_code == 404

    def test_delete_user_with_invalid_id(self):
        """Test deletion with an invalid user ID"""

        self.api_client.force_authenticate(user=self.mock_user)
        response = self.api_client.delete(self.invalid_id_url)
        assert response.status_code == 404
