# Generated by Django 2.2.17 on 2022-12-20 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_publicexperience_title_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicexperience',
            name='abuse',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicexperience',
            name='drug',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicexperience',
            name='mentalhealth',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicexperience',
            name='negbody',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicexperience',
            name='other',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicexperience',
            name='violence',
            field=models.BooleanField(default=False),
        ),
    ]
