# Generated by Django 4.2.5 on 2023-10-10 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='стоимость'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='стоимость'),
        ),
    ]