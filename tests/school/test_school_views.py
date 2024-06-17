import pytest
from django.apps import apps
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Fixture for creating an instance of the Django test client."""
    return APIClient()


@pytest.fixture
def mock_user(db):
    """Fixture for creating a mock user for testing."""
    user = mixer.blend("users.User", roles=["super-admin"])
    yield user
    user.delete()


@pytest.fixture
def mock_school(db):
    """Fixture for creating a mock school for testing."""
    school = mixer.blend("school.School")
    yield school
    school.delete()


@pytest.mark.django_db
class TestSchoolListCreateView:
    """Tests View To List, Create And Search For Schools."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, mock_user, mock_school):
        self.api_client = api_client
        self.mock_user = mock_user
        self.mock_school = mock_school
        self.url = reverse("school-list-create")
        self.api_client.force_authenticate(user=self.mock_user)

    def test_create_school(self):
        """Test creating a new school."""

        data = {
            "name": "New Test School",
            "state": "Ogun",
            "address": "123 Test St",
        }
        response = self.api_client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]

    def test_list_schools_unauthorized(self):
        """Test Unauthorized access to list schools."""

        self.api_client.logout()
        response = self.api_client.get(self.url)
        assert response.status_code == 401

    def test_list_schools_authorized(self):
        """Test Authorized access to list schools."""

        response = self.api_client.get(self.url)
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_search_schools_by_name(self):
        """Test searching schools by name."""

        self.mock_school.name = "New Test School"
        self.mock_school.save()
        print(f"Saved mock_school: {self.mock_school.name}")
        response = self.api_client.get(self.url, {"name": "test"})
        assert response.status_code == 200
        print("response data ----- ", response.data)
        assert any(
            school["name"] == self.mock_school.name for school in response.data if response.data
        )


@pytest.mark.django_db
class TestSchoolRetrieveUpdateDestroyView:
    """Tests for SchoolRetrieveUpdateDestroyView."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, mock_user, mock_school):
        self.api_client = api_client
        self.mock_user = mock_user
        self.mock_school = mock_school
        self.url = reverse(
            "school-retrieve-update-destroy",
            kwargs={"id": self.mock_school.id},
        )
        self.invalid_id_url = reverse(
            "school-retrieve-update-destroy",
            kwargs={"id": "308f5fc8-ff04-4c1d-bc6d-ea1dab4343c1"},
        )

        self.api_client.force_authenticate(user=self.mock_user)

    def test_retrieve_school_unauthorized(self):
        """Test Unauthorized access to retrieve a school."""

        self.api_client.logout()
        response = self.api_client.get(self.url)
        assert response.status_code == 401

    def test_retrieve_school_authorized(self):
        """Test Authorized access to retrieve a school."""

        response = self.api_client.get(self.url)
        assert response.status_code == 200
        assert response.data["id"] == str(self.mock_school.id)
        assert response.data["name"] == self.mock_school.name

    def test_retrieve_school_with_invalid_id(self):
        """Test retrieval with an invalid school ID"""

        response = self.api_client.get(self.invalid_id_url)
        assert response.status_code == 404

    def test_update_school_authorized(self):
        """Test authorized update of a school."""

        data = {
            "name": "Updated School Name",
            "state": "Lagos",
        }
        response = self.api_client.put(self.url, data)
        assert response.status_code == 200
        assert response.data["name"] == data["name"]

        # Fetch updated school
        updated_response = self.api_client.get(self.url)
        assert updated_response.data["name"] == data["name"]

    def test_delete_school_authorized(self):
        """Test authorized deletion of a school."""

        response = self.api_client.delete(self.url)
        assert response.status_code == 204
        School = apps.get_model("school", "School")
        school_exists = School.objects.filter(id=self.mock_school.id).exists()
        assert not school_exists
