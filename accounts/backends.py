from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q

class EmailOrMobileNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            users = UserModel.objects.filter(Q(contact_number__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            for user in users:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None