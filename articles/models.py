from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.utils.text import slugify

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

class TopicFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'topic')

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='article_set')
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
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
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
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'article')

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_as_author', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author
    class Meta:
        db_table = "comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')  # Prevent multiple favorites for the same article
        db_table = "favorite"
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"

class Report(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')  # Ensure a user can only report an article once

    def __str__(self):
        return f"{self.user.username} reported {self.article.title}"








