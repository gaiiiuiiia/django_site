from typing import Callable
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.common import WebDriverException
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
    @staticmethod
    def wait_for(
            callback: callable,
            limit: float = 5,
            tick: float = 0.3,
    ) -> Callable:
        def inner_wrapper(*args, **kwargs) -> None:
            start_time = time.time()
            while True:
                try:
                    return callback(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > limit:
                        raise e
                    time.sleep(tick)

        return inner_wrapper

    def check_row_in_list_table(self, row_text: str) -> None:
        table = self._browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def setUp(self) -> None:
        self._browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self._browser.quit()
