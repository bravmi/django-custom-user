import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import is_password_usable
from django.db.utils import IntegrityError
from django.test import TestCase

UserModel = get_user_model()


class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = UserModel.objects.create_user(email='user@gmail.com', password='foo')
        assert user.email == 'user@gmail.com'
        assert user.username is None

        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

        with pytest.raises(TypeError):
            UserModel.objects.create_user()
        with pytest.raises(ValueError):
            UserModel.objects.create_user(email='')
        with pytest.raises(ValueError):
            UserModel.objects.create_user(email='', password="foo")

    def test_create_user_with_empty_password(self):
        user = UserModel.objects.create_user(email='user@gmail.com', password=None)
        assert is_password_usable(user.password) is False

    def test_create_superuser(self):
        admin = UserModel.objects.create_superuser(email='admin@gmail.com', password='foo')
        assert admin.email == 'admin@gmail.com'
        assert admin.username is None

        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_email_unique(self):
        UserModel.objects.create_user(email='user@gmail.com', password='foo')
        with pytest.raises(IntegrityError):
            UserModel.objects.create_user(email='user@gmail.com', password='foo')

    def test_username_unique(self):
        UserModel.objects.create_user(email='user1@gmail.com', username='user', password='foo')
        with pytest.raises(IntegrityError):
            UserModel.objects.create_user(email='user2@gmail.com', username='user', password='foo')

    def test_username_unique_none(self):
        UserModel.objects.create_user(email='user1@gmail.com', password='foo')
        UserModel.objects.create_user(email='user2@gmail.com', password='foo')
        assert UserModel.objects.count() == 2

    def test_login_with_email(self):
        email = 'user@gmail.com'
        password = 'foo'
        UserModel.objects.create_user(email=email, password=password)
        assert self.client.login(username=email, password=password) is True

    def test_login_with_empty_username(self):
        email = 'user@gmail.com'
        password = 'foo'
        UserModel.objects.create_user(email=email, password=password)
        assert self.client.login(username=None, password=password) is False

    def test_login_with_username(self):
        email = 'user@gmail.com'
        username = 'user'
        password = 'foo'
        UserModel.objects.create_user(email=email, username=username, password=password)
        assert self.client.login(username=username, password=password) is True
