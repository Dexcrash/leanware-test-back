# Generated by Django 4.2.1 on 2023-05-22 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_check',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_tip',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quantity',
            name='quantiy',
            field=models.IntegerField(default=1),
        ),
    ]
