# Generated by Django 5.1.1 on 2024-10-02 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='title',
        ),
    ]
