# Generated by Django 4.0.1 on 2022-01-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_address_country_alter_address_full_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='house_building_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
