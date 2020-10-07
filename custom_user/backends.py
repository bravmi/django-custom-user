from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailUsernameBackend(ModelBackend):
    """
    Allows a user to sign in using either email/password pair or
    username/password pair
    """

    def authenticate(self, request, username=None, password=None):
        if not username:
            return None

        user = UserModel.objects.get_or(email=username) or UserModel.objects.get_or(username=username)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
