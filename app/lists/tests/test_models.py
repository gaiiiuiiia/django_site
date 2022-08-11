from django.test import TestCase

from lists.models import Item
from lists.models import List


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
