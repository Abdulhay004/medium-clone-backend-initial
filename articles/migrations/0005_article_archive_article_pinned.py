# Generated by Django 5.1.1 on 2024-10-21 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_pin_remove_article_archive_remove_article_pinned'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
