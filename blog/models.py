from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
)


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_articles')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def get_absolute_url(self):
        return '/article/%s/' % self.slug

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Article, self).save(self)

    def __str__(self):
        return self.title
