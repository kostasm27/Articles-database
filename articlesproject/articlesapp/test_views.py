from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from articlesapp.models import Article


class ArticleViewSetTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test", password="123")
        self.user2 = User.objects.create_user(username="test1", password="456")
        self.article = Article.objects.create(
            identifier="article1",
            publication_date="2025-03-19",
            abstract="Cook",
            title="Steak",
            tags="Meat, Beef, Grill",
        )
        self.article.authors.add(self.user1)
        self.article_url = reverse("article-list")
        self.article_detail_url = reverse("article-detail", args=[self.article.id])

    def test_list_articles(self):
        response = self.client.get(self.article_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_article(self):
        self.client.login(username="test", password="123")
        payload = {
            "identifier": "article2",
            "publication_date": "2025-03-20",
            "authors": [self.user1.id],
            "abstract": "abstract",
            "title": "Title",
            "tags": "Tag",
        }
        response = self.client.post(self.article_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["identifier"], "article2")

    def test_update_article_only_author(self):
        self.client.login(username="test1", password="456")
        response = self.client.patch(self.article_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test", password="123")
        response = self.client.patch(
            self.article_detail_url, {"title": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "test")

    def test_delete_article_only_author(self):
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
            tags="tag",
        )
        self.article.authors.add(self.user)
        self.download_url = reverse("article-download-csv")

    def test_download_csv(self):
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
            tags="tag",
        )
        self.payload = {"article": self.article.id, "content": "comment"}
        self.article.authors.add(self.user1)
        self.comment_url = reverse("comment-list")

    def test_create_comment(self):
        self.client.login(username="test1", password="456")
        response = self.client.post(self.comment_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "comment")

    def test_update_comment_only_owner(self):
        self.client.login(username="test1", password="456")
        response = self.client.post(self.comment_url, self.payload, format="json")
        comment_id = response.data["id"]

        self.client.login(username="test", password="123")
        comment_detail_url = reverse("comment-detail", args=[comment_id])
        response = self.client.patch(
            comment_detail_url, {"content": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test1", password="456")
        response = self.client.patch(
            comment_detail_url, {"content": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "test")

    def test_delete_comment_only_owner(self):
        self.client.login(username="test1", password="456")
        response = self.client.post(self.comment_url, self.payload, format="json")
        comment_id = response.data["id"]

        self.client.login(username="test", password="123")
        comment_detail_url = reverse("comment-detail", args=[comment_id])
        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test1", password="456")
        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
