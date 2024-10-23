# Generated by Django 4.2.16 on 2024-10-23 09:37

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.indexes
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('first_name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='first name')),
                ('first_name_uz', models.CharField(blank=True, max_length=150, null=True, verbose_name='first name')),
                ('first_name_ru', models.CharField(blank=True, max_length=150, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('last_name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='last name')),
                ('last_name_uz', models.CharField(blank=True, max_length=150, null=True, verbose_name='last name')),
                ('last_name_ru', models.CharField(blank=True, max_length=150, null=True, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('middle_name_en', models.CharField(blank=True, max_length=30, null=True)),
                ('middle_name_uz', models.CharField(blank=True, max_length=30, null=True)),
                ('middle_name_ru', models.CharField(blank=True, max_length=30, null=True)),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=['top', 'left'], force_format=None, keep_meta=True, quality=80, scale=1, size=[300, 300], upload_to=users.models.file_upload)),
                ('birth_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2024)])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('less_recommend', models.ManyToManyField(blank=True, related_name='less_recommendations', to='articles.article')),
                ('more_recommend', models.ManyToManyField(blank=True, related_name='more_recommendations', to='articles.article')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Recommendation',
                'verbose_name_plural': 'Recommendations',
                'db_table': 'recommendation',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_read', models.DateField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'article')},
            },
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'article')},
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, null=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('avatar', models.URLField(max_length=500, null=True)),
                ('followee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'follow',
                'unique_together': {('follower', 'followee')},
            },
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=django.contrib.postgres.indexes.HashIndex(fields=['first_name'], name='customuser_first_name_hash_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=django.contrib.postgres.indexes.HashIndex(fields=['last_name'], name='customuser_last_name_hash_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=django.contrib.postgres.indexes.HashIndex(fields=['middle_name'], name='customuser_middle_name_hash_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['username'], name='customuser_username_idx'),
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.CheckConstraint(check=models.Q(('birth_year__gt', 1900), ('birth_year__lt', 2024)), name='check_birth_year_range'),
        ),
    ]
