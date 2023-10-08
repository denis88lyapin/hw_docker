# Generated by Django 4.2.5 on 2023-10-03 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')),
                ('payment_amount', models.PositiveIntegerField(verbose_name='сумма оплаты')),
                ('method', models.CharField(choices=[('cash', 'наличными'), ('transfer', 'перевод')], max_length=20, verbose_name='способ оплаты:')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
            },
        ),
    ]