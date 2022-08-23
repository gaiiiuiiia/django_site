from typing import Optional

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticateBackend
from accounts.models import Token

User = get_user_model()


class TestAuthenticate(TestCase):
    def authenticate(self, uid: str) -> Optional[User]:
        request = self.client.request().wsgi_request
        return PasswordlessAuthenticateBackend().authenticate(request, uid=uid)

    def test_returns_None_if_no_such_token(self) -> None:
        self.assertIsNone(self.authenticate('no_such_token'))

    def test_returns_new_user_with_correct_email_if_token_exists(self) -> None:
        email = 'steewejoe@gmail.com'
        token = Token.objects.create(email=email)
        user = self.authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self) -> None:
        email = 'steewejoe@gmail.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = self.authenticate(token.uid)
        self.assertEqual(existing_user, user)


class TestGetUser(TestCase):
    def test_gets_user_by_email(self) -> None:
        correct_email = 'steewejoe@gmail.com'
        User.objects.create(email='some@mail.com')
        desired_user = User.objects.create(email=correct_email)
        user = PasswordlessAuthenticateBackend().get_user(correct_email)
        self.assertEqual(desired_user, user)

    def test_returns_None_if_not_user_with_that_email(self) -> None:
        self.assertIsNone(
            PasswordlessAuthenticateBackend().get_user('steewejoe@gmail.com')
        )
