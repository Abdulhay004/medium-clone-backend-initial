# Generated by Django 5.1.1 on 2024-10-11 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_remove_comment_author_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]