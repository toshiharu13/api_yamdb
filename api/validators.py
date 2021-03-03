from django.core.validators import ValidationError
from django.utils import timezone


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Введите корректный год!',
            params={'value': value},
        )
