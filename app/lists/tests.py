from django.http import HttpResponse
from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_home_page_returns_correct_html(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self) -> None:
        first_item = Item()
        first_item.text = 'First item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'First item')
        self.assertEqual(saved_items[1].text, 'Second item')

class ListViewTest(TestCase):
    def test_uses_list_template(self) -> None:
        response = self.client.get('/lists/unique_list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_all_items(self) -> None:
        Item.objects.create(text='first item')
        Item.objects.create(text='second item')

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
