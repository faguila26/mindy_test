# Generated by Django 4.2.9 on 2025-03-18 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='next_available_slot',
            new_name='next_hour',
        ),
    ]
