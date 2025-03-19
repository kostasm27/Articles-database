from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from articlesapp.models import Article, Author, Tag

class ArticleViewSetTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test", password="123")
        self.user2 = User.objects.create_user(username="test1", password="456")

        self.author1 = Author.objects.create(name="test_author")
        self.tag1 = Tag.objects.create(name="Python")
        self.article = Article.objects.create(
            identifier="article1",
            publication_date="2025-03-19",
            abstract="test",
            title="test",
            user=self.user1  
        )
        self.article.authors.add(self.author1)
        self.article.tags.add(self.tag1)
        self.article_list_url = reverse("article-list")
        self.article_detail_url = reverse("article-detail", args=[self.article.id])

    def test_list_articles(self):
        self.client.login(username="test", password="123")
        response = self.client.get(self.article_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_article(self):
        self.client.login(username="test", password="123")
        data = {
            "identifier": "article2",
            "publication_date": "2025-03-20",
            "abstract": "abstract",
            "title": "test",
            "authors": [
                {"name": "New Author"}  
            ],            
            "tags": [
                {"name": "Flask"}       
            ]  
        }

        response = self.client.post(self.article_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["identifier"], "article2")

    def test_update_article_only_owner(self):
        self.client.login(username="test1", password="456")
        response = self.client.patch(self.article_detail_url, {"title": "test_update"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test", password="123")
        response = self.client.patch(self.article_detail_url, {"title": "test_update"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "test_update")

    def test_delete_article_only_owner(self):
        self.client.login(username="test1", password="456")
        response = self.client.delete(self.article_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test", password="123")
        response = self.client.delete(self.article_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DownloadCSVTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.article = Article.objects.create(
            identifier="csv",
            publication_date="2025-03-19",
            abstract="csv",
            title="csv",
            user=self.user
        )
        self.download_url = reverse("article-download-csv")

    def test_download_csv(self):
        self.client.login(username="test", password="123")
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            'attachment; filename="articles.csv"',
            response.get("Content-Disposition", ""),
        )
        self.assertIn("text/csv", response.get("Content-Type", ""))
        csv_content = response.content.decode("utf-8")
        self.assertIn("csv", csv_content)


class CommentViewSetTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test", password="123")
        self.user2 = User.objects.create_user(username="test1", password="456")

        self.article = Article.objects.create(
            identifier="article3",
            publication_date="2025-03-19",
            abstract="test",
            title="test",
            user=self.user1
        )
        self.comment_url = reverse("comment-list")

    def test_create_comment(self):
        self.client.login(username="test1", password="456")
        data = {
            "article": self.article.id,
            "content": "new comment"
        }
        response = self.client.post(self.comment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "new comment")

    def test_update_comment_only_owner(self):
        self.client.login(username="test1", password="456")
        data = {"article": self.article.id, "content": "comment"}
        response = self.client.post(self.comment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment_id = response.data["id"]

        self.client.login(username="test", password="123")
        comment_detail_url = reverse("comment-detail", args=[comment_id])
        response = self.client.patch(comment_detail_url, {"content": "new comment"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test1", password="456")
        response = self.client.patch(comment_detail_url, {"content": "new comment"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "new comment")

    def test_delete_comment_only_owner(self):
        self.client.login(username="test1", password="456")
        data = {"article": self.article.id, "content": "delete"}
        response = self.client.post(self.comment_url, data, format="json")
        comment_id = response.data["id"]

        self.client.login(username="test", password="123")
        comment_detail_url = reverse("comment-detail", args=[comment_id])
        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test1", password="456")
        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
