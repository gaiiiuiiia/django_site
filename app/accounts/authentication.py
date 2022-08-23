from typing import Optional

from django.http import HttpRequest

from accounts.models import Token, User


class PasswordlessAuthenticateBackend:
    def authenticate(
            self,
            request: HttpRequest,
            uid: str = '',
            **kwargs,
    ) -> Optional[User]:
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return

    def get_user(self, email: str) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
