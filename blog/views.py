from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseNotFound

from .models import Article, STATUS
from .forms import ArticleForm


class IndexView(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_at')[:3]
    template_name = 'blog/pages/index.html'
    context_object_name = 'articles'


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/article/show.html'

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if article.status != STATUS[1][0]:
            return HttpResponseNotFound("Article does not exists")
        return super(ArticleDetailView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='get')
class ArticleUpdateView(generic.UpdateView):
    model = Article
    template_name = 'blog/article/edit.html'
    form_class = ArticleForm

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if request.user != article.author and (not request.user.is_superuser):
            return redirect('homepage', permanent=True)
        return super().get(self, request)


@method_decorator(login_required, name='get')
class ArticleCreateView(generic.CreateView):
    model = Article
    template_name = 'blog/article/create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return redirect(article.get_absolute_url())
