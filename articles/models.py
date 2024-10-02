from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
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
    content = models.TextField()
    status = models.CharField(max_length=20)
    thumbnail = models.ImageField(upload_to='articles/thumbnails/', null=True)
    views_count = models.IntegerField(default=0)
    reads_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topics = models.ManyToManyField(Topic, related_name='articles')

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



