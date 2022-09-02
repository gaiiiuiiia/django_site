import unittest
from unittest.mock import patch, Mock

from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from accounts.models import User
from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
)
from lists.models import Item
from lists.models import List
from lists.views import new_list


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


class NewListViewIntegratedTest(TestCase):
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

    @patch('lists.views.redirect')
    @patch('lists.views.List')
    @patch('lists.views.ItemForm')
    def test_list_owner_is_saved_if_user_is_authenticated(
            self,
            mock_item_form_class,
            mock_list_class,
            mock_redirect,
    ) -> None:
        request = HttpRequest()
        request.POST['text'] = 'some text'
        request.user = Mock()

        mock_list = mock_list_class.return_value
        # проверим, что установка пользователя произошла до сохранения объекта списка
        mock_list.save.side_effect = lambda: self.assertEqual(mock_list.owner, request.user)
        new_list(request)

        self.assertEqual(mock_list.owner, request.user)
        mock_list.save.assert_called_once_with()


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['text'] = 'some text'
        self.request.user = Mock()

    def get_mock_form(self, mock_new_list_form) -> unittest.mock.Mock:
        mock_form = mock_new_list_form.return_value
        # because redirect(obj) raises TypeError if obj is mock
        mock_form.save_with_owner.return_value.get_absolute_url.return_value = 'fakeurl'
        return mock_form

    def test_passes_POST_data_to_NewListForm(self, mock_new_list_form) -> None:
        self.get_mock_form(mock_new_list_form)
        new_list(self.request)
        mock_new_list_form.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_is_form_is_valid(self, mock_new_list_form) -> None:
        mock_form = self.get_mock_form(mock_new_list_form)
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save_with_owner.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_is_valid(self, mock_redirect, mock_new_list_form) -> None:
        mock_form = self.get_mock_form(mock_new_list_form)
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save_with_owner.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_if_from_is_not_valid(self, mock_render, mock_new_list_form) -> None:
        mock_form = self.get_mock_form(mock_new_list_form)
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'lists/home.html', {'form': mock_form})


class TestUserList(TestCase):
    def test_user_list_url_renders_user_list_template(self) -> None:
        user = User.objects.create(email='mail@me.com')
        response = self.client.get(reverse(
            'lists.user_list', kwargs={'email': user.email}
        ))
        self.assertTemplateUsed(response, 'lists/user_list.html')

    def test_passing_correct_owner_to_template(self) -> None:
        User.objects.create(email='wrong@email.com')
        correct_user = User.objects.create(email='correct@email.com')
        response = self.client.get(reverse(
            'lists.user_list', kwargs={'email': correct_user.email}
        ))
        self.assertEqual(response.context['owner'], correct_user)
