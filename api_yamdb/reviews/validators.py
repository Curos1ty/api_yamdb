import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверка года выпуска произведения."""
    current_year = dt.date.today().year
    if value > current_year:
        raise ValidationError('Год выпуска не может превышать текущий год!')
    return value
