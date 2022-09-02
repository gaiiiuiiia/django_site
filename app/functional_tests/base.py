from typing import Callable
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Keys, FirefoxOptions
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

    @wait()
    def wait_to_be_logged_in(self, email: str) -> None:
        self.wait_for(lambda: self._browser.find_element(By.LINK_TEXT, 'Log out'))()
        navbar = self._browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait()
    def wait_to_be_logged_out(self, email: str) -> None:
        self.wait_for(lambda: self._browser.find_element(By.NAME, 'email'))()
        navbar = self._browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)

    def enter_and_submit_list_item(
            self,
            item_text: str,
            check_creating: bool = True
    ) -> None:
        current_item_count = len(self._browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr'))
        input_box = self.get_item_input_box()
        input_box.send_keys(item_text)
        input_box.send_keys(Keys.ENTER)
        if check_creating:
            self.wait_for(self.check_row_in_list_table)(f'{current_item_count + 1}: {item_text}')

    def check_row_in_list_table(self, row_text: str) -> None:
        table = self._browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self) -> WebElement:
        return self._browser.find_element(By.ID, 'id_text')

    def setUp(self) -> None:
        options = FirefoxOptions()
        options.add_argument('--headless')
        self._browser = webdriver.Firefox(options=options)

    def tearDown(self) -> None:
        self._browser.quit()
