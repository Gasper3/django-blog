from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Article


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
        if request.user != article.author and (not request.user.is_superuser):
            return redirect('homepage', permanent=True)
        return super().get(self, request)

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)
        article.title = request.POST['article_title']
        article.content = request.POST['article_content']
        article.save()
        return render(request, self.template_name, {
            'article': article,
            'message': "Article edited"
        })
