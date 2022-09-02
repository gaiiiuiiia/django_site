import unittest
from unittest.mock import patch, Mock

from django.test import TestCase
from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, NewListForm,
)
from lists.models import List, Item


class ItemFormTest(TestCase):
    def test_form(self) -> None:
        form = ItemForm()

        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())

    def test_form_validation_for_blank_items(self) -> None:
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_save_items_using_form(self) -> None:
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'some text'})
        form.save_for_list(list_)

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'some text')
        self.assertEqual(Item.objects.first().list, list_)


class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self) -> None:
        list_ = List.objects.create()
        form = ExistingListItemForm(list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self) -> None:
        list_ = List.objects.create()
        form = ExistingListItemForm(list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self) -> None:
        similar_text = 'There is similar text'
        list_ = List.objects.create()
        Item.objects.create(text=similar_text, list=list_)
        form = ExistingListItemForm(list_, data={'text': similar_text})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(self, mock_list_create_new) -> None:
        user = Mock(is_authenticated=False)
        text = 'some text'
        form = NewListForm(data={'text': text})
        form.is_valid()
        form.save_with_owner(owner=user)
        mock_list_create_new.assert_called_once_with(first_item_text=text)

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_is_authenticated(self, mock_list_create_new) -> None:
        user = Mock(is_authenticated=True)
        text = 'some text'
        form = NewListForm(data={'text': text})
        form.is_valid()
        form.save_with_owner(owner=user)
        mock_list_create_new.assert_called_once_with(first_item_text=text, owner=user)

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_list_create_new) -> None:
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'some text'})
        form.is_valid()
        list_ = form.save_with_owner(user)

        self.assertEqual(list_, mock_list_create_new.return_value)
