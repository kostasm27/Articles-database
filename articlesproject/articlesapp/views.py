from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse
import csv
from rest_framework.exceptions import PermissionDenied

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from .filters import ArticleFilter


class ArticlePagination(PageNumberPagination):
    """
        Pagination Class
    """
    page_size = 100
    page_query_param = "page"
    page_size_query_param = "page_size"


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ArticleFilter
    search_fields = ["title", "abstract"]
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Args:
            serializer (ArticleSerializer)

        Raises:
            PermissionDenied: If the requesting user is not among the article's authors.
        """
        article = self.get_object()
        if self.request.user not in article.authors.all():
            raise PermissionDenied(
                "An article that was not written by you cannot be updated."
            )
        serializer.save()

    def perform_destroy(self, serializer):
        """
        Args:
            serializer (ArticleSerializer)

        Raises:
            PermissionDenied: If the requesting user is not among the article's authors.
        """
        article = self.get_object()
        if self.request.user not in article.authors.all():
            raise PermissionDenied(
                "An article that was not written by you cannot be deleted."
            )
        serializer.save() 

    @action(detail=False, methods=["get"])
    def download_csv(self, request):
        """
        Custom action to download a CSV of filtered articles.

        Returns:
            HttpResponse: A CSV file with article data.
        """
        articles = self.get_queryset()
        articles = self.filter_queryset(articles)
        if authors := request.query_params.get("authors"):
            articles = articles.filter(authors__in=authors)

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="articles.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(
            ["Identifier", "Title", "Publication Date", "Authors", "Tags", "Abstract"]
        )

        for article in articles:
            authors_str = ", ".join([user.username for user in article.authors.all()])
            writer.writerow(
                [
                    article.identifier,
                    article.title,
                    article.publication_date,
                    authors_str,
                    article.tags,
                    article.abstract,
                ]
            )
        return response


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Raises:
            PermissionDenied: If the requesting user is not the comment's owner.
        """
        comment = self.get_object()
        if comment.user != self.request.user:
            raise PermissionDenied("You cannot update someone else's comment.")
        serializer.save()

    def perform_destroy(self, serializer):
        """
        Raises:
            PermissionDenied: If the requesting user is not the comment's owner.
        """
        comment = self.get_object()
        if comment.user != self.request.user:
            raise PermissionDenied("You cannot delete someone else's comment.")
        serializer.save()
