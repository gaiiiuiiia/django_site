from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from selenium.webdriver.common.by import By

from .base import FunctionalTest

User = get_user_model()


class TestUserList(FunctionalTest):
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

    def test_logged_it_users_see_their_email(self) -> None:
        email = 'steewejoe@gmail.com'
        self._browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        self.create_pre_authenticated_session(email)
        self._browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_saved_as_my_lists(self) -> None:
        # Айгуль авторизована в системе
        email = 'aigul@the.best'
        self.create_pre_authenticated_session(email)
        self._browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

        # Она начинает создавать новый список дел
        self.enter_and_submit_list_item('solaris')
        self.enter_and_submit_list_item('genesis')
        first_lists_url = self._browser.current_url

        # И замечает кнопку "Мои списки"
        btn_my_lists = self._browser.find_element(By.ID, 'id_my_lists')

        # Она с непреодолимым интересом кликает на эту кнопку и видит,
        # что на этой странице отображен ее список с названием в честь первого элемента ее списка
        btn_my_lists.click()
        self.wait_for(lambda: self._browser.find_element(By.LINK_TEXT, 'solaris'))()
        self._browser.find_element(By.LINK_TEXT, 'solaris').click()
        self.wait_for(lambda: self.assertEqual(self._browser.current_url, first_lists_url))()

        # Она возвращается на главную
        self._browser.get(self.live_server_url)

        # и создает новый список
        self.enter_and_submit_list_item('new horizon')
        self.enter_and_submit_list_item('sharpy eyes')
        second_list_url = self._browser.current_url

        # Потом чтобы убедиться в том, что ее списки создались, она опять кликает на кнопку мои списки
        self._browser.find_element(By.ID, 'id_my_lists').click()

        # И уже ее встречают два ее списка
        self.wait_for(lambda: self._browser.find_element(By.LINK_TEXT, 'solaris'))()
        self.wait_for(lambda: self._browser.find_element(By.LINK_TEXT, 'new horizon'))()

        self._browser.find_element(By.LINK_TEXT, 'new horizon').click()

        self.wait_for(lambda: self.assertEqual(self._browser.current_url, second_list_url))()

        # Она выходит из системы и больше не видит кнопку "Мои списки"
        self._browser.find_element(By.CLASS_NAME, 'btn-logout').click()

        self.wait_for(lambda: self.assertEqual(
            self._browser.find_elements(By.ID, 'id_my_lists'),
            []
        ))()

        self.fail('End Test')
