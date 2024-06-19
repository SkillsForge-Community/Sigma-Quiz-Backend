# Generated by Django 4.2 on 2024-06-19 13:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("quiz", "0002_alter_quiz_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Round",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("round_number", models.PositiveIntegerField()),
                ("no_of_questions", models.PositiveIntegerField()),
                ("no_of_schools", models.PositiveIntegerField()),
                ("marks_per_question", models.PositiveIntegerField()),
                ("marks_per_bonus_question", models.PositiveIntegerField()),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rounds",
                        to="quiz.quiz",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("question_number", models.PositiveIntegerField()),
                ("correct_answer", models.CharField(blank=True, max_length=255, null=True)),
                ("answered_by", models.CharField(blank=True, max_length=100, null=True)),
                ("bonus_to", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="round.round",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddConstraint(
            model_name="round",
            constraint=models.UniqueConstraint(
                fields=("quiz", "round_number"), name="unique_school_quiz_round"
            ),
        ),
    ]