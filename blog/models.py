from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
)


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True

    def get_absolute_url(self):
        return '/article/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content
