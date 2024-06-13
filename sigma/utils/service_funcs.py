from django.core.exceptions import ValidationError


def default_roles():
    """Returns adhoc as default incase of no choice"""

    return ["adhoc"]


def validate_roles(value):
    """
    Validates that the input value is a list of strings, and all strings
    are among the valid role choices.
    """

    if not isinstance(value, list):
        raise ValidationError("Roles must be a list.")
    valid_choices = {"quiz-master", "adhoc", "super-admin"}
    invalid_roles = [role for role in value if role not in valid_choices]

    for role in value:
        if not isinstance(role, str):
            raise ValidationError("Each role must be a string")
    if invalid_roles:
        raise ValidationError(
            f"Invalid role(s): {', '.join(invalid_roles)}. "
            f"Allowed roles: {', '.join(valid_choices)}."
        )
