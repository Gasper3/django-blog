from django.forms import ModelForm, Textarea, TextInput, Select
from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'status']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
        }
