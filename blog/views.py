from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Article

from pprint import pprint


class IndexView(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/pages/index.html'
    context_object_name = 'articles'


class ArticleShowView(generic.DetailView):
    model = Article
    template_name = 'blog/article/show.html'


@method_decorator(login_required, name='get')
class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/article/edit.html'

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs['slug'])
        pprint(article)
        if request.user != article.author:
            return redirect('homepage', permanent=True)
        return super().get(self, request)
