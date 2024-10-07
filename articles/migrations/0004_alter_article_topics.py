# Generated by Django 5.1.1 on 2024-10-02 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='topics',
            field=models.ManyToManyField(related_name='articles', to='articles.topic'),
        ),
    ]