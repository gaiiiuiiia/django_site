from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class TestItemValidation(FunctionalTest):
    def test_cannot_add_empty_list_items(self) -> None:
        # Эдит открывает домашнюю страницу и случайно пытается отправить пустой элемент списка
        self._browser.get(self.live_server_url)
        self._browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        # Домашняя страница обновляется, и появляется сообщение об ошибке, которое гласит,
        # что элементы списка не должны совпадать
        self.wait_for(
            lambda: self.assertEqual(
                self._browser.find_element(By.CSS_SELECTOR, '.has-error').text,
                'You can`t have empty list item'
            )
        )()

        # Она отправляет корректный элемент, и все срабатывает
        self._browser.find_element(By.ID, 'id_new_item').send_keys('Not empty')
        self._browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        self.wait_for(self.check_row_in_list_table)('1: Not empty')

        # Эдит пытается еще раз отправить пустой элемент, однако сайт ее снова предупреждает об ошибке
        self._browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self._browser.find_element(By.CSS_SELECTOR, '.has-error').text,
                'You can`t have empty list item'
            )
        )()