from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse

from accounts.models import User


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self) -> str:
        return reverse('lists.view', kwargs={'list_id': self.id})

    @staticmethod
    def create_new(
            first_item_text: str,
            owner: User = None
    ) -> List:
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    @property
    def name(self):
        return self.item_set.first().text
