import datetime

from django.core.exceptions import ValidationError


def validation_year(value):
    year_now = datetime.datetime.now().year
    if value > year_now:
        raise ValidationError(f'Год выпуска не может быть больше {year_now}')
