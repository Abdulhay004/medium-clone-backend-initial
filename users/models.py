from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils import timezone

from django.contrib.postgres.indexes import HashIndex
from .errors import BIRTH_YEAR_ERROR_MSG

from articles.models import Article, Author

User = settings.AUTH_USER_MODEL

import os
import uuid

def file_upload(instance, filename):
    """ This function is used to upload the user's avatar. """
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    return os.path.join('users/avatars/', filename)

class CustomUser(AbstractUser):
    """  This model represents a custom user. """
    # article = models.Fore
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    # avatar = models.ImageField(upload_to=file_upload, blank=True)
    avatar = ResizedImageField(size=[300, 300], crop=['top', 'left'], upload_to=file_upload, blank=True)

    birth_year = models.IntegerField(
        validators=[  # tug'ilgan yil oralig'ini tekshirish uchun birinchi variant
            validators.MinValueValidator(settings.BIRTH_YEAR_MIN),
            validators.MaxValueValidator(settings.BIRTH_YEAR_MAX)
        ],
        null=True,
        blank=True
    )

    def clean(self):  # tug'ilgan yil oralig'ini tekshirish uchun ikkinchi variant
        super().clean()
        if self.birth_year and not (settings.BIRTH_YEAR_MIN < self.birth_year < settings.BIRTH_YEAR_MAX):
            raise ValidationError(BIRTH_YEAR_ERROR_MSG)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

        # Composite Index va Hash Index qo'shish
        indexes = [
            HashIndex(fields=['first_name'], name='%(class)s_first_name_hash_idx'),
            HashIndex(fields=['last_name'], name='%(class)s_last_name_hash_idx'),
            HashIndex(fields=['middle_name'], name='%(class)s_middle_name_hash_idx'),
            models.Index(fields=['username'], name='%(class)s_username_idx'),
        ]

        constraints = [
            models.CheckConstraint(
                check=models.Q(birth_year__gt=settings.BIRTH_YEAR_MIN) &
                      models.Q(birth_year__lt=settings.BIRTH_YEAR_MAX),
                name='check_birth_year_range'
            )
        ]



    def __str__(self):
        """ This method returns the full name of the user"""
        if self.full_name:
            return self.full_name
        else:
            return self.email or self.username


    @property
    def full_name(self):
        """ Returns the user's full name. """
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class ArticleStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISH = 'publish', 'Published'
    ARCHIVE = 'archive', 'Archived'
class Recommendation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    more_recommend = models.ManyToManyField(Article, related_name='more_recommendations', blank=True)
    less_recommend = models.ManyToManyField(Article, related_name='less_recommendations', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "recommendation"
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"
        ordering = ["-created_at"]

class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_read = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')  # Ensure a user can only read an article once

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, null=True)
    followee = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=150, null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(null=True)
    avatar = models.URLField(max_length=500, null=True)
    class Meta:
        db_table = 'follow'
        unique_together = ('follower', 'followee')

    def __str__(self):
        return f"{self.follower}"

class Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'article')  # Уникальная пара: пользователь-статья
    def __str__(self):
        return f"{self.user.username} pinned {self.article.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.message


