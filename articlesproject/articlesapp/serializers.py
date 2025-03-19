from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    """
        Article Serializer
    """
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Article
        fields = [
            "id",
            "identifier",
            "publication_date",
            "authors",
            "abstract",
            "title",
            "tags",
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
        Comment Serializer
    """
    class Meta:
        model = Comment
        fields = [
            "id",
            "article",
            "user",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]
