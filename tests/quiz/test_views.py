from datetime import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from sigma.quiz.models import SchoolRegisteredForQuiz
from tests.authentication.factories import UserModelFactory
from tests.quiz.factories import QuizFactory, SchoolRegisteredForQuizFactory
from tests.rounds.factories import RoundFactory
from tests.school.factories import SchoolFactory


class RegisterSchoolForQuizViewTests(APITestCase):

    def setUp(self):
        self.user = UserModelFactory()
        self.quiz = QuizFactory(date=datetime.today())
        self.round = RoundFactory(
            quiz=self.quiz,
            round_number=3,
            no_of_questions=3,
            no_of_schools=3,
            marks_per_question=4,
            marks_per_bonus_question=3,
        )
        self.school_1 = SchoolFactory()
        self.school_2 = SchoolFactory(name="God's grace", state="Lagos")
        self.url = reverse("list_create_school_for_quiz", args=[self.quiz.id])

    def test_school_is_registered_for_quiz_with_valid_data(self):
        """Test school is registered for quiz with valid data"""
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, data={"school_id": self.school_1.id}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(SchoolRegisteredForQuiz.objects.first())

    def test_errror_raised_if_school_registered_already(self):
        """Test error raised if school registered already"""
        SchoolRegisteredForQuizFactory(quiz=self.quiz, school=self.school_1)

        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, data={"school_id": self.school_1.id}, format="json")

        self.assertEqual(response.status_code, 409)

    def test_schools_registered_for_quiz_are_retrieved(self):
        """Test schools registered for quiz are retrieved"""
        SchoolRegisteredForQuizFactory(quiz=self.quiz, school=self.school_1)
        SchoolRegisteredForQuizFactory(quiz=self.quiz, school=self.school_2)

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 2)


class UnRegisterSchoolForQuizViewTests(APITestCase):

    def setUp(self):
        self.user = UserModelFactory()
        self.quiz = QuizFactory(date=datetime.today())
        self.school_1 = SchoolFactory()
        self.school_2 = SchoolFactory(name="James School", address="Ibadan")
        self.school_for_quiz_1 = SchoolRegisteredForQuizFactory(
            quiz=self.quiz, school=self.school_1
        )
        self.school_for_quiz_2 = SchoolRegisteredForQuizFactory(
            quiz=self.quiz, school=self.school_2
        )
        self.url = reverse("unregister_school_for_quiz", args=[self.quiz.id, self.school_1.id])

    def test_school_is_unregistered_for_quiz(self):
        """Test school unregistered for quiz"""
        self.client.force_authenticate(self.user)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(SchoolRegisteredForQuiz.objects.filter(school=self.school_1).first())
        self.assertEqual(SchoolRegisteredForQuiz.objects.count(), 1)
