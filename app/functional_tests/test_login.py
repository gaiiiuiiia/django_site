import re

from django.core import mail
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest

TEST_EMAIL = 'steewejoe@gmail.com'


class TestLogin(FunctionalTest):

    def test_can_get_email_link_to_log_in(self) -> None:
        # Айгуль заходит на сайт с заметками и видит поле для ввода email
        # Она вводит свою почту и нажимает enter
        self._browser.get(self.live_server_url)
        self._browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self._browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # Она видит сообщение, которое оповещает ее, что письмо успешно отправлено
        self.wait_for(lambda: self.assertIn(
            'Mail successfully send',
            self._browser.find_element(By.TAG_NAME, 'body').text)
        )()

        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)

        url_search = re.search(r'http://.+/.+', email.body)
        if not url_search:
            self.fail('No site url found')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Айгуль переходит по ссылке
        self._browser.get(url)

        # После перехода по ссылке она попадает на страницу сайта. Она в системе!
        self.wait_for(lambda: self._browser.find_element(By.LINK_TEXT, 'Log out'))()
        navbar = self._browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # Айгуль хочет выйти из своей учетной записи и нажимает на кнопку выйти
        self._browser.find_element(By.LINK_TEXT, 'Log out').click()

        self.wait_for(lambda: self._browser.find_element(By.NAME, 'email'))()
        navbar = self._browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)
