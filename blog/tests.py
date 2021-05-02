from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from pprint import pprint

from blog.models import Article, Comment


def create_article(title, content, author, is_deleted=False, status=1) -> Article:
    return Article.objects.create(title=title, content=content, author=author, status=status, is_deleted=is_deleted)


def create_comment_to_article(article: Article, content, author: User, is_deleted=False) -> Comment:
    return Comment.objects.create(article=article, content=content, author=author, is_deleted=is_deleted)


def create_superuser(username) -> User:
    return User.objects.create_superuser(username, 'admin@example.com', 'qwe')


def create_user(username) -> User:
    return User.objects.create_user(username, 'user@example.com', 'qwe')


class IndexViewTests(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['articles'], [])

    def test_one_deleted(self):
        user = create_user('user')
        create_article('NonDeleted', 'asd', user, False, 1)
        create_article('NonDeleted2', 'asd', user, False, 1)
        create_article('Deleted', 'asd', user, True, 1)

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 2)

    def test_deleted_and_draft(self):
        user = create_user('user')
        create_article('NonDeleted', 'asd', user, False, 1)
        create_article('NonDeletedDraft', 'asd', user, False, 0)
        create_article('Deleted', 'asd', user, True, 1)

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 1)


class ArticleDetailViewTests(TestCase):
    def test_article_show(self):
        user = create_user('user')
        article = create_article('Article title', 'content', user)

        url = reverse('article_show', args=(article.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article title')
        self.assertContains(response, user.first_name)

    def test_article_wrong_status(self):
        user = create_user('user')
        article = create_article('Article title', 'content', user, status=0)

        url = reverse('article_show', args=(article.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_comments(self):
        user = create_user('user')
        comment_author = create_user('Comment author')
        article = create_article('Article title', 'content', user)

        comment1 = create_comment_to_article(article, 'Nice article', comment_author)
        comment2 = create_comment_to_article(article, 'Nicely done', comment_author)
        comment3 = create_comment_to_article(article, 'Wow! Nice!', comment_author)

        url = reverse('article_show', args=(article.slug,))
        response = self.client.get(url)
        comments = response.context['comments']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(comments), 3)
        # TODO - assert objects not contents if its possible
        self.assertQuerysetEqual(comments, [comment3.content, comment2.content, comment1.content], transform=str)

    def test_comments_deleted(self):
        user = create_user('user')
        comment_author = create_user('Comment author')
        article = create_article('Article title', 'content', user)

        create_comment_to_article(article, 'Nice article', comment_author, True)
        comment = create_comment_to_article(article, 'Nicely done', comment_author)
        create_comment_to_article(article, 'Wow! Nice!', comment_author, True)

        url = reverse('article_show', args=(article.slug,))
        response = self.client.get(url)
        comments = response.context['comments']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(comments), 1)
        # TODO - assert objects not contents if its possible
        self.assertQuerysetEqual(comments, [comment.content], transform=str)


class ArticleUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = create_superuser('admin')
        cls.user = create_user('user')

    def test_not_logged_in(self):
        article = create_article('Article title', 'Content', self.admin)

        url = reverse('article_edit', args=(article.slug,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_logged_user(self):
        article = create_article('Article title', 'Content', self.user)

        url = reverse('article_edit', args=(article.slug,))
        is_logged = self.client.login(username=self.user.username, password='qwe')
        if is_logged:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['article'].title, article.title)
        else:
            raise self.failureException('User is not logged in')

    def test_logged_user_no_permissions(self):
        article = create_article('Article title', 'Content', self.admin)

        url = reverse('article_edit', args=(article.slug,))
        is_logged = self.client.login(username=self.user.username, password='qwe')
        if is_logged:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 301)
        else:
            raise self.failureException('User is not logged in')

    def test_logged_superuser_not_author(self):
        article = create_article('Article title', 'Content', self.user)

        url = reverse('article_edit', args=(article.slug,))
        is_logged = self.client.login(username=self.admin.username, password='qwe')
        if is_logged:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['article'].title, article.title)
        else:
            raise self.failureException('User is not logged in')

