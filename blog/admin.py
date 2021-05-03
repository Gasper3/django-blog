from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status',)
    list_display = ('title', 'status', 'author', 'created_at')
    list_editable = ('status',)
    search_fields = ('title', 'created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'article', 'author', 'created_at', 'is_deleted',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
