# Generated by Django 4.2.1 on 2023-05-22 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Quantities',
            new_name='Quantity',
        ),
    ]
