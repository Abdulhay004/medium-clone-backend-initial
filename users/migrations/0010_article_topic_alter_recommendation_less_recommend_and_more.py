# Generated by Django 5.1.1 on 2024-10-04 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_recommendation_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='less_recommend',
            field=models.ManyToManyField(blank=True, related_name='less_recommendations', to='users.article'),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='more_recommend',
            field=models.ManyToManyField(blank=True, related_name='more_recommendations', to='users.article'),
        ),
        migrations.AddField(
            model_name='article',
            name='topics',
            field=models.ManyToManyField(to='users.topic'),
        ),
    ]
