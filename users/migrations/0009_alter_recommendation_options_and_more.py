# Generated by Django 5.1.1 on 2024-10-04 12:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_rename_userprofile_recommendation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recommendation',
            options={'ordering': ['-created_at'], 'verbose_name': 'Recommendation', 'verbose_name_plural': 'Recommendations'},
        ),
        migrations.AddField(
            model_name='recommendation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterModelTable(
            name='recommendation',
            table='recommendation',
        ),
    ]
