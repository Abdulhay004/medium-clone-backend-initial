# Generated by Django 5.1.1 on 2024-10-10 21:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_follow'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follow',
            new_name='TopicFollow',
        ),
    ]
