# Generated by Django 5.1.1 on 2024-10-15 15:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0027_favoritearticle'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavoriteArticle',
            new_name='Favorite',
        ),
        migrations.RenameField(
            model_name='clap',
            old_name='claps_count',
            new_name='count',
        ),
    ]