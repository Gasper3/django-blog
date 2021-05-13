from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='homepage'),
    path('article/<slug:slug>', ArticleDetailView.as_view(), name='article_show'),
    path('article/edit/<slug:slug>', ArticleUpdateView.as_view(), name='article_edit'),
    path('article/create', ArticleCreateView.as_view(), name='article_create'),
    path('comment/create', CommentCreateView.as_view(), name='comment_create'),
    path('articles', AllArticlesView.as_view(), name='all_articles')
]
