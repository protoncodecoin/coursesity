from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp) -> str:
        return str(user.pk) + str(timestamp) + str(user.is_active)
    

generate_token = TokenGenerator()