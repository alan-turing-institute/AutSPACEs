# Generated by Django 2.2.17 on 2023-01-23 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20230123_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicexperience',
            old_name='approved',
            new_name='moderation_status',
        ),
    ]
