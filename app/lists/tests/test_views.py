from unittest import skip

from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
)
from lists.models import Item
from lists.models import List


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_home_page_returns_correct_html(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self) -> None:
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            reverse('lists.view', kwargs={'list_id': list_.id}),
            data={'text': ''}
        )

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

    def test_can_save_a_POST_request_to_an_existing_list(self) -> None:
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            reverse('lists.view', kwargs={'list_id': correct_list.id}),
            data={'text': 'A new item for existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self) -> None:
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            reverse('lists.view', kwargs={'list_id': correct_list.id}),
            data={'text': 'A new item for existing list'}
        )

        self.assertRedirects(
            response,
            reverse('lists.view', kwargs={'list_id': correct_list.id})
        )

    def test_display_item_form(self) -> None:
        list_ = List.objects.create()
        response = self.client.get(
            reverse('lists.view', kwargs={'list_id': list_.id})
        )

        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_invalid_input_nothing_save_to_db(self) -> None:
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self) -> None:
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_invalid_input_renders_form_template(self) -> None:
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_input_show_error_on_page(self) -> None:
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplication_error_end_up_on_lists_page(self) -> None:
        similar_text = 'similar text'
        error_text = escape(DUPLICATE_ITEM_ERROR)

        list_ = List.objects.create()
        Item.objects.create(text=similar_text, list=list_)
        response = self.client.post(
            reverse('lists.view', kwargs={'list_id': list_.id}),
            data={'text': similar_text}
        )

        self.assertContains(response, error_text)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self) -> None:
        self.client.post(
            reverse('lists.new'),
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self) -> None:
        response = self.client.post(
            reverse('lists.new'),
            data={'text': 'A new list item'}
        )
        new_list = List.objects.first()

        self.assertRedirects(
            response,
            reverse('lists.view', kwargs={'list_id': new_list.id})
        )

    def test_validation_errors_are_sent_back_to_home_page_template(self) -> None:
        response = self.client.post(
            reverse('lists.new'),
            data={'text': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

        # escape - экранизация символов
        expected_error = escape("You can`t have empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_input_renders_home_template(self) -> None:
        response = self.client.post(
            reverse('lists.new'),
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_invalid_input_have_validation_message(self) -> None:
        response = self.client.post(
            reverse('lists.new'),
            data={'text': ''}
        )
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_invalid_input_have_item_form(self) -> None:
        response = self.client.post(
            reverse('lists.new'),
            data={'text': ''}
        )
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_items_arent_saved(self) -> None:
        self.client.post(
            reverse('lists.new'),
            data={'text': ''}
        )

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
