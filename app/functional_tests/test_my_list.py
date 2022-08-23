from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest

User = get_user_model()


class TestMyList(FunctionalTest):
    def create_pre_authenticated_session(self, email: str) -> None:
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## установить cookie, которые нужны для первого посещения домена
        ## а страница 404 загружается быстрее всего
        self._browser.get(f'{self.live_server_url}/abracadabra/404')
        self._browser.add_cookie({
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'path': '/',
        })

    def test_logged_in_user_lists_are_saved_as_my_list(self) -> None:
        email = 'steewejoe@gmail.com'
        self._browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        self.create_pre_authenticated_session(email)
        self._browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
