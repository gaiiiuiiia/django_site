# Generated by Django 4.0.6 on 2022-08-17 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_list_item_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('list', 'text')},
        ),
    ]
