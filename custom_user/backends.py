from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailUsernameBackend(ModelBackend):
    """
    Allows a user to sign in using either email/password pair or
    username/password pair
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            return None

        if '@' in username:
            user = self.get_user_or(email=username)
        else:
            user = self.get_user_or(username=username)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user_or(self, default=None, **fields):
        try:
            return UserModel.objects.get(**fields)
        except UserModel.DoesNotExist:
            return default
