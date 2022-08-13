from django.test import TestCase
from lists.forms import ItemForm


class ItemFormTest(TestCase):
    def test_form(self) -> None:
        form = ItemForm()

        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control"', form.as_p())
        self.fail(form.as_p())
