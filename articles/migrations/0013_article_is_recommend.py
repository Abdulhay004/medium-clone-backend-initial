# Generated by Django 5.1.1 on 2024-10-04 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_clap_claps_count_clap_comments_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_recommend',
            field=models.BooleanField(default=False),
        ),
    ]
