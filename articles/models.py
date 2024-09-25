
from django.db import models


class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
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
    thumbnail = models.ImageField(upload_to="thumbs", editable=False)

class Article(models.Model):
    # about = models.ForeignKey(About, on_delete=models.CASCADE)
    # topics = models.ForeignKey(Topics, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    midle_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    avatar = models.ImageField(null=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'article'
        verbose_name = 'Article'
        ordering = ["-created_at"]

class Clap(models.Model):
    pass



