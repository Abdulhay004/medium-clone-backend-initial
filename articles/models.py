
from django.db import models
from datetime import datetime



class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'topic'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ["name"]

class About(models.Model):
    ORDER_STATUS = ((0, 'Started'), (1, 'Done'), (2, 'Error'))
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=500)
    content = models.CharField(max_length=500)
    status = models.SmallIntegerField(choices=ORDER_STATUS)

class Article(models.Model):
    # about = models.ForeignKey(About, on_delete=models.CASCADE)
    # topics = models.ForeignKey(Topics, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    # avatar = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=False)
    # updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'article'
        verbose_name = 'Article'
        ordering = ["-created_at"]
        verbose_name_plural = "Articles"


class Clap(models.Model):
    pass



