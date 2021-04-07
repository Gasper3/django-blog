from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='homepage'),
    path('article/<slug:slug>/', views.ArticleShowView.as_view(), name='article_show'),
    path('article/edit/<slug:slug>', views.ArticleDetailView.as_view(), name='article_edit')
]
