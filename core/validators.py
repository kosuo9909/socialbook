from django.core.exceptions import ValidationError


def validate_letters(value):
    for ch in value:
        if not ch.isalnum():
            raise ValidationError('Please input letters and numbers only.')