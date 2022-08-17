from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse

from lists.models import Item
from lists.models import List


class ListModelTest(TestCase):
    def test_get_absolute_url(self) -> None:
        list_ = List.objects.create()
        self.assertEqual(
            list_.get_absolute_url(),
            reverse('lists.view', kwargs={'list_id': list_.id})
        )


class ItemModelTest(TestCase):
    def test_item_default_text(self) -> None:
        item = Item()
        self.assertEqual(item.text, '')

    def test_cant_save_item_with_empty_text(self) -> None:
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='')

        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_item_is_related_to_list(self) -> None:
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertEqual(item.list, list_)

    def test_cant_save_duplicate_items(self) -> None:
        similar_text = 'There is similar text'
        list_ = List.objects.create()
        Item.objects.create(text=similar_text, list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text=similar_text, list=list_)
            item.full_clean()

    def test_can_save_similar_items_on_different_lists(self) -> None:
        similar_text = 'Another similar text'
        Item.objects.create(text=similar_text, list=List.objects.create())
        item = Item.objects.create(text=similar_text, list=List.objects.create())

        # Ошибки быть не должно
        item.full_clean()
