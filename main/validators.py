import unicodedata

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str


@deconstructible
class FullnameValidator(validators.RegexValidator):
    """
    Validator for person fullname.

    Note:
        Pattern for person fullname: "^[А-ЯA-Za-zа-я- ]+\Z"

    """
    regex = r'^[А-ЯA-Za-zа-я- ]+\Z'
    message = (
        'Введите валидное ФИО. Это поле может содержать только русские символы, - и пробельные символы '
    )
    flags = 0


@deconstructible
class BaseFieldValidator:
    """
    Validator that does not allow control characters and characters provided in blacklist_str field.

    Attributes:
        message (str): Message if validation fails
        code (str): Validation error code
        blacklist_str (str or None): String with characters that cannot be provided

    """
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
    """
    Validator for title.

    Note:
        Blacklist characters: [!\"'$^;?*,<>]

    """
    message = "В этом поле не разрешены управляющие символы, а также символы {!\\\"'$^;?*,<>}"
    blacklist_str = r"!\"'$^;?*,<>"
