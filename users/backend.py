from django.contrib.auth.backends import BaseBackend

class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        None
    def get_user(user_id=''):
        None