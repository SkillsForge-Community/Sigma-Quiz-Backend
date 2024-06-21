from rest_framework import serializers

from .models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [
            "name",
            "state",
            "address",
            "id",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        request = self.context.get("request")

        if not request or request.method in ["GET", "PUT"]:
            fields = ["id", "name", "state", "address"]
        else:
            fields = self.Meta.fields

        representation = super().to_representation(instance)
        return {field: representation[field] for field in fields if field in representation}
