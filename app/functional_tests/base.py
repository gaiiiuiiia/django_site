from typing import Callable
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.common import WebDriverException
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def wait(
        limit_time: float = 5,
        tick_time: float = 0.3
) -> Callable:
    def decorator(callback: callable) -> Callable:
        def wrapper(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return callback(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > limit_time:
                        raise e
                    time.sleep(tick_time)
        return wrapper
    return decorator


class FunctionalTest(StaticLiveServerTestCase):
    @staticmethod
    def wait_for(callback: callable) -> Callable:
        @wait()
        def wrapper(*args, **kwargs) -> None:
            callback(*args, **kwargs)
        return wrapper

    def wait_to_be_logged_in(self, email: str) -> None:
        self.wait_for(lambda: self._browser.find_element(By.LINK_TEXT, 'Log out'))()
        navbar = self._browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email: str) -> None:
        self.wait_for(lambda: self._browser.find_element(By.NAME, 'email'))()
        navbar = self._browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)

    def check_row_in_list_table(self, row_text: str) -> None:
        table = self._browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self) -> WebElement:
        return self._browser.find_element(By.ID, 'id_text')

    def setUp(self) -> None:
        self._browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self._browser.quit()
