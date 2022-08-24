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
        self.enter_and_submit_list_item('new list item')

        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            BROWSER_WIDTH / 2,
            delta=10
        )
