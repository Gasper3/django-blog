from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Article, Comment


def create_article(title, content, author, is_deleted, status) -> Article:
    return Article.objects.create(title=title, content=content, author=author, status=status, is_deleted=is_deleted)


def create_comment_to_article(article: Article, content, author: User) -> Comment:
    return Comment.objects.create(article=article, content=content, author=author)


class IndexViewTests(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['articles'], [])

    def test_one_deleted(self):
        user = User.objects.create_user('admin', 'admin@example.com', 'qwe')
        create_article('NonDeleted', 'asd', user, False, 1)
        create_article('NonDeleted2', 'asd', user, False, 1)
        create_article('Deleted', 'asd', user, True, 1)

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 2)

    def test_deleted_and_draft(self):
        user = User.objects.create_user('admin', 'admin@example.com', 'qwe')
        create_article('NonDeleted', 'asd', user, False, 1)
        create_article('NonDeletedDraft', 'asd', user, False, 0)
        create_article('Deleted', 'asd', user, True, 1)

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 1)
