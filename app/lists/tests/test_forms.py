from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
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
