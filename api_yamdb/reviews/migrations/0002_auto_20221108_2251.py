# Generated by Django 2.2.16 on 2022-11-08 19:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Значение меньше минимального.Значение должно быть от 1 до 10'), django.core.validators.MaxValueValidator(10, message='Значение больше максимального.Значение должно быть от 1 до 10')]),
        ),
    ]
