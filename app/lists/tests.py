from django.test import TestCase
from django.urls import reverse

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
        list_ = List.objects.create()
        response = self.client.get(
            reverse('lists.view', kwargs={'list_id': list_.id})
        )
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_items_only_for_that_list(self) -> None:
        correct_list = List.objects.create()
        Item.objects.create(text='first item', list=correct_list)
        Item.objects.create(text='second item', list=correct_list)

        another_list = List.objects.create()
        Item.objects.create(text='another text', list=another_list)

        response = self.client.get(
            reverse('lists.view', kwargs={'list_id': correct_list.id})
        )

        self.assertContains(response, 'first item')
        self.assertContains(response, 'second item')
        self.assertNotContains(response, 'another text')


    def test_passes_correct_list_to_template(self) -> None:
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(
            reverse('lists.view', kwargs={'list_id': correct_list.id})
        )

        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self) -> None:
        self.client.post(
            reverse('lists.new'),
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self) -> None:
        response = self.client.post(
            reverse('lists.new'),
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()

        self.assertRedirects(
            response,
            reverse('lists.view', kwargs={'list_id': new_list.id})
        )


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self) -> None:
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            reverse('lists.add', kwargs={'list_id': correct_list.id}),
            data={'item_text': 'A new item for existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self) -> None:
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            reverse('lists.add', kwargs={'list_id': correct_list.id}),
            data={'item_text': 'A new item for existing list'}
        )

        self.assertRedirects(
            response,
            reverse('lists.view', kwargs={'list_id': correct_list.id})
        )
