import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_.]{1,150}$', value) is None:
        raise ValidationError(f'Недопустимые символы <{value}>.')
    return value
