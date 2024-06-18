from rest_framework import serializers

from .models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "year",
            "title",
            "description",
            "date",
            "id",
            "created_at",
            "updated_at",
        ]

    def get_year(self, obj):
        return str(obj.date.year)

    def to_representation(self, instance):
        request = self.context.get("request")
        if request.method in ["GET", "PUT"]:
            fields = ["id", "year", "title", "description", "date"]
        else:
            fields = self.Meta.fields

        representation = super().to_representation(instance)
        return {field: representation[field] for field in fields if field in representation}
