from django import forms
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

    def save_for_list(self, list_: List) -> None:
        self.instance.list = list_
        return super().save()
