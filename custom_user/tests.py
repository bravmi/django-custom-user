import pytest
from django.contrib.auth.hashers import is_password_usable
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from .models import User


class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='user@gmail.com', password='foo')
        assert user.email == 'user@gmail.com'
        assert user.username is None

        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

        with pytest.raises(TypeError):
            User.objects.create_user()
        with pytest.raises(ValueError):
            User.objects.create_user(email='')
        with pytest.raises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_user_with_empty_password(self):
        user = User.objects.create_user(email='user@gmail.com', password=None)
        assert is_password_usable(user.password) is False

    def test_create_superuser(self):
        admin = User.objects.create_superuser(email='admin@gmail.com', password='foo')
        assert admin.email == 'admin@gmail.com'
        assert admin.username is None

        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_email_unique(self):
        User.objects.create_user(email='user@gmail.com', password='foo')
        with pytest.raises(IntegrityError):
            User.objects.create_user(email='user@gmail.com', password='foo')

    def test_username_unique(self):
        User.objects.create_user(email='user1@gmail.com', username='user', password='foo')
        with pytest.raises(IntegrityError):
            User.objects.create_user(email='user2@gmail.com', username='user', password='foo')

    def test_username_unique_none(self):
        User.objects.create_user(email='user1@gmail.com', password='foo')
        User.objects.create_user(email='user2@gmail.com', password='foo')
        assert User.objects.count() == 2

    def test_emails_different_case(self):
        User.objects.create_user(email='user@gmail.com', password='foo')
        with pytest.raises(IntegrityError):
            User.objects.create_user(email='USER@gmail.com', password='foo')


class EmailUsernameBackendTests(TestCase):
    def test_login_with_email(self):
        email = 'user@gmail.com'
        password = 'foo'
        User.objects.create_user(email=email, password=password)
        assert self.client.login(username=email, password=password) is True

    def test_login_with_email_uppercase(self):
        email = 'user@gmail.com'
        password = 'foo'
        User.objects.create_user(email=email, password=password)
        assert self.client.login(username=email.upper(), password=password) is True

    def test_login_with_empty_username(self):
        email = 'user@gmail.com'
        password = 'foo'
        User.objects.create_user(email=email, password=password)
        assert self.client.login(username=None, password=password) is False

    def test_login_with_username(self):
        email = 'user@gmail.com'
        username = 'user'
        password = 'foo'
        User.objects.create_user(email=email, username=username, password=password)
        assert self.client.login(username=username, password=password) is True

    def test_invalid_username(self):
        user = User.objects.create_user(email='user@gmail.com', username='@user', password='foo')
        with pytest.raises(ValidationError, match=r'Enter a valid username'):
            user.full_clean()
