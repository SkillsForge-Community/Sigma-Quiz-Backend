from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as password_validator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

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
        """validates provided password"""
        try:
            password_validator(password=value)
        except ValidationError as err:
            raise serializers.ValidationError(err.messages, code="Invalid Password")
        return value

    def validate_roles(self, value):
        """Validates role"""

        valid_roles = ["quiz-master", "adhoc", "super-admin"]

        if value[0] not in valid_roles:
            raise serializers.ValidationError("Forbidden: super-admin Only", code="Forbidden")

        return value

    def create(self, validated_data):
        """Creates user account"""

        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])

        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "roles"]


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs["email"]).first()

        if user is None:
            raise serializers.ValidationError("User doesn't exist", code="Bad Request")

        if user and not user.check_password(attrs["password"]):
            raise serializers.ValidationError("Wrong credentials provided", code="Bad Request")

        if user and user.check_password(attrs["password"]):
            return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {"access_token": str(refresh.access_token), "user": ProfileSerializer(instance).data}


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        """This is for validating email"""

        user = User.objects.filter(email=value).first()

        if user is None:
            raise serializers.ValidationError("User doesn't exist", code="Not Found")

        return value

    def validate_new_password(self, value):
        """This is for validating new password"""

        user = self.context["request"].user

        if user.check_password(value):
            raise serializers.ValidationError(
                "New password can't be same as Old password", code="Invalid Password"
            )
        try:
            password_validator(value)
        except ValidationError as err:
            raise serializers.ValidationError(err.messages, code="Invalid Password")

        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        """This is for validating old password"""

        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Wrong Old Password", code="Invalid Password")

        return value

    def validate_new_password(self, value):
        """This is for validating new password"""

        user = self.context["request"].user

        if user.check_password(value):
            raise serializers.ValidationError(
                "New password can't be same as Old password", code="Invalid Password"
            )
        try:
            password_validator(value)
        except ValidationError as err:
            raise serializers.ValidationError(err.messages, code="Invalid Password")

        return value
