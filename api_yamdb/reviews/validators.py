import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверка года выпуска произведения."""
    current_year = dt.date.today().year
    if value > current_year:
        raise ValidationError('Год выпуска не может превышать текущий год!')
    return value


# def validate_score(value):
#     """Проверка соответствия рейтинга значению 1-10."""
#     if not 0 < isinstance(value, int) < 11:
#         raise ValueError(
#             'Значение рейтинга должно быть целым числом в диапазоне 1-10!'
#         )
#     return value
