# Generated by Django 4.0.1 on 2022-01-27 11:07

import django.core.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='address',
            name='full_address',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='address',
            name='house_building_number',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.MaxValueValidator(99999)]),
        ),
        migrations.AlterField(
            model_name='address',
            name='pin_code',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999), django.core.validators.MinValueValidator(10000)]),
        ),
    ]