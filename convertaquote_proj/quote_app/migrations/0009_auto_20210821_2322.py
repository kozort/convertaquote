# Generated by Django 2.2 on 2021-08-21 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_app', '0008_quote_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='added_item',
            name='package',
            field=models.CharField(max_length=45),
        ),
    ]
