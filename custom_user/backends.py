from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

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

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
