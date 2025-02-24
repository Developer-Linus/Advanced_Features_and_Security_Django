from django.contrib.auth.backends import BaseBackend

class EmailBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None):
        #Implement logic to authenticate users using email and password.
        return 
    def get_user(self, user_id):
       #implement logic to return user based on User Id
       return 