from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, call

from accounts.models import Token
from lib.helper_functions import url_with_querystring


class TestSendLoginEmail(TestCase):
    TEST_EMAIL = 'steewejoe@gmail.com'

    def submit_send_mail_form(self):
        return self.client.post(
            reverse('accounts.send_login_email'),
            data={'email': self.TEST_EMAIL}
        )

    def test_redirects_to_home_page(self) -> None:
        response = self.submit_send_mail_form()
        self.assertRedirects(response, reverse('home'))

    @patch('accounts.views.send_mail')
    def test_send_mail_from_POST(self, mock_send_mail) -> None:
        self.submit_send_mail_form()
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link')
        self.assertEqual(to_list, ['steewejoe@gmail.com'])

    def test_adds_success_message(self) -> None:
        response = self.client.post(
            reverse('accounts.send_login_email'),
            data={'email': self.TEST_EMAIL},
            follow=True
        )
        message = list(response.context['messages'])[0]

        self.assertEqual(
            message.message,
            'Mail successfully send'
        )
        self.assertEqual(message.tags, "success")

    def test_create_token_associated_with_user_email(self) -> None:
        self.submit_send_mail_form()
        token = Token.objects.first()
        self.assertEqual(token.email, self.TEST_EMAIL)

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_id(self, mock_send_mail) -> None:
        self.submit_send_mail_form()
        token = Token.objects.first()
        expected_url = url_with_querystring(
            reverse('accounts.login'),
            token=token.uid
        )
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class TestLogin(TestCase):
    def test_redirects_to_home(self, mock_auth) -> None:
        response = self.client.get(
            url_with_querystring(
                reverse('accounts.login'),
                token='sometoken',
            )
        )

        self.assertRedirects(response, reverse('home'))

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth) -> None:
        token = 'sometoken'
        self.client.get(url_with_querystring(reverse('accounts.login'), token=token))
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid=token)
        )

    def test_calls_auth_with_user_if_there_is_one(self, mock_auth) -> None:
        response = self.client.get(url_with_querystring(reverse('accounts.login'), token='sometoken'))
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth) -> None:
        mock_auth.authenticate.return_value = None
        self.client.get(url_with_querystring(reverse('accounts.login'), token='sometoken'))
        self.assertFalse(mock_auth.login.called)
