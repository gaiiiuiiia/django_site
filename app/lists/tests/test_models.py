from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse

from lists.models import Item
from lists.models import List

User = get_user_model()


class ListModelTest(TestCase):
    def test_get_absolute_url(self) -> None:
        list_ = List.objects.create()
        self.assertEqual(
            list_.get_absolute_url(),
            reverse('lists.view', kwargs={'list_id': list_.id})
        )

    def test_create_new_creates_list_and_first_item(self) -> None:
        text = 'some text'
        List.create_new(first_item_text=text)
        new_list = List.objects.first()
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self) -> None:
        text = 'some text'
        user = User.objects.create()
        List.create_new(first_item_text=text, owner=user)
        self.assertEqual(List.objects.first().owner, user)

    def test_lists_can_have_owners(self) -> None:
        # Не должно поднять исключение
        List(owner=User())

    def test_list_owner_is_optional(self) -> None:
        # Не должно поднять исключение
        List().full_clean()

    def test_create_new_returns_new_list_object(self) -> None:
        returned = List.create_new(first_item_text='some text')
        list_ = List.objects.first()
        self.assertEqual(returned, list_)

    def test_list_name_is_first_item_text(self) -> None:
        first_item_text = 'first item text'
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=first_item_text)
        Item.objects.create(list=list_, text='another text')
        self.assertEqual(list_.name, first_item_text)


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
