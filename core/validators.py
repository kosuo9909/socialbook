from django.core import exceptions


def validate_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise exceptions.ValidationError('Please input letters only.')