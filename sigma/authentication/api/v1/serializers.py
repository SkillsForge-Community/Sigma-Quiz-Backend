from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "roles",
            "password",
            "created_at",
            "updated_at",
        ]

    def validate_email(self, value):
        """Validate provided email"""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f"Key (email)=({value}) already exists.", code="Bad Request"
            )
        return value

    def validate_password(self, value):
        """Validates provided password"""

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be minimum of eight(8) characters", code="Short Password"
            )
        return value

    def validate_roles(self, value):
        """Validates role"""

        if value[0] != "super-admin":
            raise serializers.ValidationError("Forbidden: super-admin Only", code="Forbidden")

        return value

    def create(self, validated_data):
        """Creates user account"""

        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])

        return user
