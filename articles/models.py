from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import uuid

User = settings.AUTH_USER_MODEL

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
class Topic(models.Model):
    name = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True, null=True)
    # description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'topic'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ["name"]

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="author")
    summary = models.TextField()
    content = RichTextField()
    slug = models.SlugField(unique=True, blank=True)
    STATUS_CHOICES = [
        ('active', 'ACTIVE'),
        ('trash', 'TRASH'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    thumbnail = models.ImageField(upload_to='articles/thumbnails/', null=True)
    views_count = models.IntegerField(default=0)
    reads_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topics = models.ManyToManyField(Topic, related_name='articles')
    is_recommend = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically generate slug from title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = 'Article'
        ordering = ["-created_at"]
        verbose_name_plural = "Articles"


class Clap(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comments_count = models.PositiveIntegerField(default=0)
    claps_count = models.PositiveIntegerField(default=0)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"
    class Meta:
        db_table = "comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]





