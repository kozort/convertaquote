# Generated by Django 2.2 on 2021-08-21 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_app', '0006_auto_20210816_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='added_items',
            field=models.ManyToManyField(blank=True, related_name='quotes', to='quote_app.ADDED_ITEM'),
        ),
    ]