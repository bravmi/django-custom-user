from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

from .validators import UsernameValidator


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(email=email, username=username, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username_validator = UsernameValidator()
    username = models.CharField(max_length=150, unique=True, blank=True, null=True, validators=[username_validator])
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        if not self._state.adding:
            return

        if self.username and User.objects.filter(username__iexact=self.username).exists():
            raise ValidationError('User with this Username already exists.')
        if User.objects.filter(email__iexact=self.email).exists():
            raise ValidationError('User with this Email already exists.')

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.email
