# Generated by Django 4.2.1 on 2023-05-22 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_customer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantity',
            old_name='quantiy',
            new_name='quantity',
        ),
    ]
