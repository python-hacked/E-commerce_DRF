# Generated by Django 4.0.1 on 2022-01-27 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_user_profile_picture'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
    ]