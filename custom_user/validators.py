from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w.+-]*\Z'
    message = 'Enter a valid username. This value may contain only letters, numbers, and ./+/-/_ characters.'
    flags = 0
