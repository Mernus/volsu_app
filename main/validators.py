from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class FullnameValidator(validators.RegexValidator):
    regex = r'^[А-Яа-я-]+\Z'
    message = (
        'Введите валидное ФИО. Это поле может содержать только русские символы и -'
    )
    flags = 0
