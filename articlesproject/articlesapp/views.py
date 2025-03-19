from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv

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
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ArticlePagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ArticleFilter
    search_fields = ["title", "abstract"]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Raises:
            PermissionDenied: If the requesting user is not among the article's authors.
        """
        article = self.get_object()
        if article.user != self.request.user:
            raise PermissionDenied(
                "An article that was not written by you cannot be updated."
            )
        serializer.save()

    def perform_destroy(self, serializer):
        """
        Raises:
            PermissionDenied: If the requesting user is not among the article's authors.
        """
        article = self.get_object()
        if article.user != self.request.user:
            raise PermissionDenied(
                "An article that was not written by you cannot be deleted."
            )
        serializer.delete()

    @action(detail=False, methods=["get"])
    def download_csv(self, request):
        """
        Custom action to download a CSV of filtered articles.

        Returns:
            HttpResponse: A CSV file with article data.
        """
        articles = self.filter_queryset(self.get_queryset())

        identifiers_param = request.query_params.getlist("identifier")
        if identifiers_param:
            articles = articles.filter(identifier__in=identifiers_param)

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="articles.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(["Identifier", "Title", "Publication Date", "Authors", "Tags", "Abstract"])

        for article in articles:
            authors_str = ", ".join([author.name for author in article.authors.all()])
            tags_str = ", ".join([tag.name for tag in article.tags.all()])
            writer.writerow([
                article.identifier,
                article.title,
                article.publication_date,
                authors_str,
                tags_str,
                article.abstract,
            ])

        return response


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
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
        serializer.delete()
