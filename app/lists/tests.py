from django.test import TestCase

from lists.models import Item
from lists.models import List


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_home_page_returns_correct_html(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self) -> None:
        list_ = List.objects.create()
        first_item = Item.objects.create(text='First item', list=list_)
        second_item = Item.objects.create(text='Second item', list=list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        self.assertEqual(saved_items[0].text, 'First item')
        self.assertEqual(saved_items[1].text, 'Second item')
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].list, list_)

class ListViewTest(TestCase):
    def test_uses_list_template(self) -> None:
        response = self.client.get('/lists/unique_list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_all_items(self) -> None:
        list_ = List.objects.create()
        Item.objects.create(text='first item', list=list_)
        Item.objects.create(text='second item', list=list_)

        response = self.client.get('/lists/unique_list/')

        self.assertContains(response, 'first item')
        self.assertContains(response, 'second item')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self) -> None:
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self) -> None:
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertRedirects(response, '/lists/unique_list/')
