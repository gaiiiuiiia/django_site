from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from .base import FunctionalTest


class TestNewVisitor(FunctionalTest):
    def test_can_start_a_list_for_one_user(self) -> None:
        # Эдит слышала про крутое web приложение, напоминающее список неотложных дел
        # Она заходит на главную страницу и видит, что заголовок сайта говорит ей о списках неотложных дел
        self._browser.get(self.live_server_url)
        self.assertIn('To-Do List', self._browser.title)

        header_text = self._browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        self.assertEqual(
            self.get_item_input_box().get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья (ее хобби - вязание рыболовных мушек)"
        self.enter_and_submit_list_item('Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент
        # Она вводит "Сделать мушку из павлиньих перьев (Эдит очень методична)"
        self.enter_and_submit_list_item('Сделать мушку из павлиньих перьев')

    def test_multiple_users_can_start_list_at_different_urls(self) -> None:
        # Эдит открывает сайт со списками
        self._browser.get(self.live_server_url)

        # И создает элемент списка
        self.enter_and_submit_list_item('Элемент списка Эдит')

        # Она замечает, что ее список имеет уникальный URL-адрес
        edith_list_url = self._browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Теперь новый пользователь Френсис заходит на сайт
        ## Переоткроем браузер. Тем самым мы исключаем вероятность того, что данные Эдит попадут Френсису
        self._browser.quit()
        self._browser = webdriver.Firefox()

        # Френсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self._browser.get(self.live_server_url)
        page_text = self._browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Элемент списка Эдит', page_text)

        # Френсис начинает новый список
        self.enter_and_submit_list_item('Элемент списка Френсиса')

        # Френсис получает уникальный URL-адрес
        francis_list_url = self._browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Нет и следа от списка Эдит
        page_text = self._browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Элемент списка Френсиса', page_text)
        self.assertNotIn('Элемент списка Эдит', page_text)
