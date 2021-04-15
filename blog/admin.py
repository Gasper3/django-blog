from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
