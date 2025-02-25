from django.contrib.auth.backends import BaseBackend

class EmailBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None):
        return super().authenticate(request, username, password)
    def get_user(self, user_id):
        return super().get_user(user_id)