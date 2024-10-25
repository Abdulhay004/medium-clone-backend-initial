
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField()),
                ('content', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('status', models.CharField(choices=[('active', 'ACTIVE'), ('trash', 'TRASH')], default='active', max_length=10)),
                ('thumbnail', models.ImageField(null=True, upload_to='articles/thumbnails/')),
                ('views_count', models.IntegerField(default=0)),
                ('reads_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_recommend', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'db_table': 'article',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Clap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comments_count', models.PositiveIntegerField(default=0)),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'db_table': 'comment',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites',
                'db_table': 'favorite',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'db_table': 'topic',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TopicFollow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.topic')),
            ],
        ),
    ]
