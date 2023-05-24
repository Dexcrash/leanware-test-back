# Generated by Django 4.2.1 on 2023-05-22 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('table_id', models.IntegerField()),
                ('waiter_id', models.IntegerField()),
                ('state', models.CharField(choices=[('1', 'ORDERING'), ('2', 'CHECKING'), ('3', 'PAID')], default='1', max_length=2)),
                ('total_check', models.IntegerField(default='0')),
                ('total_tip', models.IntegerField(default='0')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_paid', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('img', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Quantities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantiy', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.product')),
            ],
        ),
    ]