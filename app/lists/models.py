from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)

class List(models.Model):
    def get_absolute_url(self) -> str:
        return reverse('lists.view', kwargs={'list_id': self.id})