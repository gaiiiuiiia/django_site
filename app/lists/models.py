from django.conf import settings
from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def name(self) -> str:
        return self.item_set.first().text

    def get_absolute_url(self) -> str:
        return reverse('lists.view', kwargs={'list_id': self.id})