# Generated by Django 5.1.1 on 2024-10-10 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_article_is_recommend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('TRASH', 'trash')], default='ACTIVE', max_length=10),
        ),
    ]
