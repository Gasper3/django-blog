from django.forms import ModelForm, Textarea, TextInput, Select, HiddenInput
from .models import Article, Comment


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'status']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': TextInput(attrs={'class': 'form-control'}),
        }
