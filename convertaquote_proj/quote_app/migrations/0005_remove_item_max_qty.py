# Generated by Django 2.2 on 2021-08-16 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quote_app', '0004_item_max_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='max_qty',
        ),
    ]
