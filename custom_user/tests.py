import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
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
        User = get_user_model()
        email = 'user@gmail.com'
        password = None
        User.objects.create_user(email=email, password=password)

    def test_create_superuser(self):
        User = get_user_model()
        admin = User.objects.create_superuser(email='admin@gmail.com', password='foo')
        assert admin.email == 'admin@gmail.com'
        assert admin.username is None

        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_email_unique(self):
        User = get_user_model()
        User.objects.create(email='user@gmail.com', password='foo')
        with pytest.raises(IntegrityError):
            User.objects.create(email='user@gmail.com', password='foo')

    def test_username_unique(self):
        User = get_user_model()
        User.objects.create(email='user1@gmail.com', password='foo')
        User.objects.create(email='user2@gmail.com', password='foo')

    def test_login_with_email(self):
        User = get_user_model()
        email = 'user@gmail.com'
        password = 'foo'
        User.objects.create_user(email=email, password=password)
        assert self.client.login(username=email, password=password) is True

    def test_login_with_empty_username(self):
        User = get_user_model()
        email = 'user@gmail.com'
        password = 'foo'
        User.objects.create_user(email=email, password=password)
        assert self.client.login(username=None, password=password) is False

    def test_login_with_username(self):
        User = get_user_model()
        email = 'user@gmail.com'
        username = 'user'
        password = 'foo'
        User.objects.create_user(email=email, username=username, password=password)
        assert self.client.login(username=username, password=password) is True
