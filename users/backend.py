from django.contrib.auth.backends import BaseBackend

class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        None
    def get_user(user_id=''):
        None

user_logged_in = False
database_manager_logged_in = False

def auth_context(request):
    return {
        "user_logged": user_logged_in,
        "manager_logged": database_manager_logged_in
    }