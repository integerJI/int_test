# Generated by Django 2.1.8 on 2020-04-11 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intworlduser', '0005_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_image',
        ),
    ]