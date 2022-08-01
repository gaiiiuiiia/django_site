import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self._browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self._browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self) -> None:
        # Эдит слышала про крутое web приложение, напоминающее список неотложных дел
        # Она заходит на главную страницу и видит, что заголовок сайта говорит ей о списках неотложных дел
        self._browser.get('http://d-webserver')
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
        time.sleep(1)

        table = self._browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(
            any(row.text == '1: Купить павлинь перья' for row in rows)
        )

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент
        # Она вводит "Сделать мушку из павлиньих перьев (Эдит очень методична)"

        # Страница снова обновляется и теперь Эдит видит оба элемента ее списка

        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что сайт сгенерировал для нее уникальный URL-адрес -
        # об этом выводится небольшой текст с пояснениями

        # Она посещает этот адрес, ее список по-прежнему там
        # Удовлетворенная, она снова ложится спать
        self.fail('End test')


if __name__ == '__main__':
    unittest.main()
