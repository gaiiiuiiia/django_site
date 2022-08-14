from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class TestLayoutAndStying(FunctionalTest):
    def test_layout_and_styling(self) -> None:
        # Эдит заходит на домашнюю страницу и видит, что поле для ввода центрировано
        self._browser.get(self.live_server_url)
        BROWSER_WIDTH = 1024
        BROWSER_HEIGHT = 768

        self._browser.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)

        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            BROWSER_WIDTH / 2,
            delta=10
        )

        # Она начинает новый список и видит, что там поле для ввода также центрировано
        input_box.send_keys('New list')
        input_box.send_keys(Keys.ENTER)
        self.wait_for(self.check_row_in_list_table)('1: New list')

        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            BROWSER_WIDTH / 2,
            delta=10
        )
