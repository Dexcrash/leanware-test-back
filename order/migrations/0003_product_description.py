# Generated by Django 4.2.1 on 2023-05-22 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_quantities_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]