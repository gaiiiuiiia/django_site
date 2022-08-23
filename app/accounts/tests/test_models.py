from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Token

User = get_user_model()


class TestUserModel(TestCase):
    def test_user_only_with_email_is_valid(self) -> None:
        user = User(email='a@b.com')
        user.full_clean()

    def test_email_is_primary_key(self) -> None:
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_no_problem_with_auth_login(self) -> None:
        user = User.objects.create(email='steewejoe@gmail.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        # не должно поднять исключение
        auth.login(request, user)


class TestTokenModel(TestCase):
    def test_links_user_with_auto_generated_uid(self) -> None:
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)