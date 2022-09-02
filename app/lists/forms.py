from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User
from lists.models import Item, List

EMPTY_ITEM_ERROR = 'You can`t have empty list item'
DUPLICATE_ITEM_ERROR = 'You already have similar item'


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control',
            })
        }
        error_messages = {
            'text': {
                'required': EMPTY_ITEM_ERROR,
            },
        }

    def save_for_list(self, list_: List) -> Item:
        self.instance.list = list_
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, list_: List, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.instance.list = list_

    def validate_unique(self) -> None:
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)


class NewListForm(ItemForm):
    def save_with_owner(self, owner: User) -> List:
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data.get('text'), owner=owner)
        return List.create_new(first_item_text=self.cleaned_data.get('text'))
