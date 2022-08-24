from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from .base import FunctionalTest


class TestItemValidation(FunctionalTest):
    def get_error_element_on_page(self) -> WebElement:
        return self._browser.find_element(By.CSS_SELECTOR, '.has-error')

    def test_cannot_add_empty_list_items(self) -> None:
        # Эдит открывает домашнюю страницу и случайно пытается отправить пустой элемент списка
        self._browser.get(self.live_server_url)
        self.enter_and_submit_list_item('', False)

        # Домашняя страница обновляется, и появляется сообщение об ошибке, которое гласит,
        # что элементы списка не должны совпадать
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element_on_page().text,
            EMPTY_ITEM_ERROR
        ))()

        # Она отправляет корректный элемент, и все срабатывает
        self.enter_and_submit_list_item('not empty')

        # Эдит пытается еще раз отправить пустой элемент, однако сайт ее снова предупреждает об ошибке
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element_on_page().text,
            EMPTY_ITEM_ERROR
        ))()

    def test_cannot_add_duplicate_items(self) -> None:
        # Айгуль открывает домашнюю страницу и создает заметку
        self._browser.get(self.live_server_url)
        self.enter_and_submit_list_item('Test')
        # Чисто по случайности она добавляет еще одну такую же запись
        self.enter_and_submit_list_item('Test', False)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element_on_page().text,
            DUPLICATE_ITEM_ERROR
        ))()

    def test_error_message_hide_when_text_filed_changing(self) -> None:
        # Айгуль открывает домашнюю страницу и создает заметку.
        self._browser.get(self.live_server_url)
        similar_text = 'I\'m a good manager'
        self.enter_and_submit_list_item(similar_text)

        # Она пытается создать такую же заметку и получает сообщение об ошибке.
        self.enter_and_submit_list_item(similar_text, False)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element_on_page().text,
            DUPLICATE_ITEM_ERROR
        ))()
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element_on_page().is_displayed()
        ))()

        # Она начинает вводить новый текст и ошибка исчезает. Айгуль очень довольна.
        self.get_item_input_box().clear()
        self.get_item_input_box().send_keys(f'{similar_text} ever')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element_on_page().is_displayed()
        ))()
