from django.urls import reverse
from rest_framework.test import APITestCase

from sigma.round.models import RoundForSchool
from tests.authentication.factories import UserModelFactory
from tests.quiz.factories import QuizFactory, SchoolRegisteredForQuizFactory
from tests.rounds.factories import RoundFactory, RoundForSchoolFactory
from tests.school.factories import SchoolFactory


class RoundForSchoolViewTests(APITestCase):

    def setUp(self):
        self.user = UserModelFactory()
        self.quiz = QuizFactory()
        self.round = RoundFactory(quiz=self.quiz)
        self.school = SchoolFactory()
        self.school_registered_for_quiz = SchoolRegisteredForQuizFactory(
            school=self.school, quiz=self.quiz
        )

        self.url = reverse("round_for_school", args=[self.round.id])

    def test_round_can_be_created_for_school_registered_for_quiz(self):
        """Test round can be created for school registered for quiz"""

        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, data={"school_id": self.school.id}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(
            RoundForSchool.objects.filter(school=self.school, round=self.round).first()
        )

    def test_round_cannot_be_created_for_school_yet_to_register_for_quiz(self):
        """Test round cannot be created for school yet to register for quiz"""

        self.school_registered_for_quiz.delete()

        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={"school_id": self.school.id}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"message": "School Not Registered for Quiz", "error": "Not Found", "statusCode": 400},
        )


class RemoveSchoolFromRoundViewTests(APITestCase):

    def setUp(self):
        self.user = UserModelFactory()
        self.quiz = QuizFactory()
        self.round = RoundFactory(quiz=self.quiz)
        self.school_1 = SchoolFactory()
        self.school_2 = SchoolFactory(name="New School")
        self.school_registered_for_quiz = SchoolRegisteredForQuizFactory(
            school=self.school_1, quiz=self.quiz
        )
        self.school_registered_for_quiz = SchoolRegisteredForQuizFactory(
            school=self.school_2, quiz=self.quiz
        )
        self.round_for_school_1 = RoundForSchoolFactory(round=self.round, school=self.school_1)
        self.round_for_school_2 = RoundForSchoolFactory(round=self.round, school=self.school_2)

        self.url = reverse("remove_schoool_from_round", args=[self.round.id, self.school_1.id])

    def test_school_can_be_removed_from_round(self):
        """Test school can be removed from round"""

        self.client.force_authenticate(self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(RoundForSchool.objects.filter(school=self.school_1).first())
