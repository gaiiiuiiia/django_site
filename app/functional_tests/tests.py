import time
from typing import Callable

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


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


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self._browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self._browser.quit()

    def check_row_in_list_table(self, row_text: str) -> None:
        table = self._browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_for_one_user(self) -> None:
        # Эдит слышала про крутое web приложение, напоминающее список неотложных дел
        # Она заходит на главную страницу и видит, что заголовок сайта говорит ей о списках неотложных дел
        self._browser.get(self.live_server_url)
        self.assertIn('To-Do List', self._browser.title)

        header_text = self._browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        input_box = self._browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья (ее хобби - вязание рыболовных мушек)"
        input_box.send_keys('Купить павлиньи перья')

        # Когда она нажимает enter, страница обновляется, и теперь страница содержит
        # "1: Купить павлиньи перья" в качестве элемента списка
        input_box.send_keys(Keys.ENTER)
        wait_for(self.check_row_in_list_table)('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент
        # Она вводит "Сделать мушку из павлиньих перьев (Эдит очень методична)"
        input_box = self._browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        input_box.send_keys(Keys.ENTER)

        # Страница снова обновляется и теперь Эдит видит оба элемента ее списка
        wait_for(self.check_row_in_list_table)('1: Купить павлиньи перья')
        wait_for(self.check_row_in_list_table)('2: Сделать мушку из павлиньих перьев')

    def test_multiple_users_can_start_list_at_different_urls(self) -> None:
        # Эдит открывает сайт со списками
        self._browser.get(self.live_server_url)

        # И создает элемент списка
        input_box = self._browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Элемент списка Эдит')
        input_box.send_keys(Keys.ENTER)
        wait_for(self.check_row_in_list_table)('1: Элемент списка Эдит')

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
        input_box = self._browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Элемент списка Френсиса')
        input_box.send_keys(Keys.ENTER)
        wait_for(self.check_row_in_list_table)('1: Элемент списка Френсиса')

        # Френсис получает уникальный URL-адрес
        francis_list_url = self._browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Нет и следа от списка Эдит
        page_text = self._browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Элемент списка Френсиса', page_text)
        self.assertNotIn('Элемент списка Эдит', page_text)

        self.fail('End test')

    def test_layout_and_styling(self) -> None:
        # Эдит заходит на домашнюю страницу и видит, что поле для ввода центрировано
        self._browser.get(self.live_server_url)
        BROWSER_WIDTH = 1024
        BROWSER_HEIGHT = 768

        self._browser.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)

        input_box = self._browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            BROWSER_WIDTH / 2,
            delta=10
        )

        # Она начинает новый список и видит, что там поле для ввода также центрировано
        input_box.send_keys('New list')
        input_box.send_keys(Keys.ENTER)
        wait_for(self.check_row_in_list_table)('1: New list')

        input_box = self._browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            BROWSER_WIDTH / 2,
            delta=10
        )

