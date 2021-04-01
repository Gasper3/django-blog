from django.shortcuts import render
from django.views import generic
from .models import Article


class IndexView(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/pages/index.html'
    context_object_name = 'articles'


class ArticleShowView(generic.DetailView):
    model = Article
    template_name = 'blog/article/show.html'


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/article/edit.html'
