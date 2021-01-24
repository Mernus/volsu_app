import unicodedata

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str


from django.core.exceptions import ValidationError


@deconstructible
class FullnameValidator(validators.RegexValidator):
    regex = r'^[А-ЯA-Za-zа-я- ]+\Z'
    message = (
        'Введите валидное ФИО. Это поле может содержать только русские символы, - и пробельные символы '
    )
    flags = 0


@deconstructible
class BaseFieldValidator:
    message = "В этом поле не разрешены управляющие символы и символы из параметра blacklist"
    code = "no_control_characters_with_blacklist"
    blacklist_str = None

    def __init__(self, message=None, code=None, blacklist_str=None):
        if message:
            self.message = message
        if code:
            self.code = code
        if blacklist_str:
            self.blacklist_str = blacklist_str

    def __call__(self, value):
        value = force_str(value)
        blacklist_str = self.blacklist_str
        category = unicodedata.category
        for character in value:
            if blacklist_str and character not in blacklist_str:
                continue
            if category(character)[0] == "C":
                params = {'value': value, 'blacklist': blacklist_str}
                raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return (
            isinstance(other, BaseFieldValidator) and
            (self.blacklist_str == other.blacklist_str) and
            (self.message == other.message) and
            (self.code == other.code)
        )


@deconstructible
class TitleValidator(BaseFieldValidator):
    message = "В этом поле не разрешены управляющие символы, а также символы {!\\\"'$^;?*,<>}"
    blacklist_str = r"!\"'$^;?*,<>"
