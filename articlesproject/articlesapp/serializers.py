from rest_framework import serializers
from .models import Article, Author, Tag, Comment

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        extra_kwargs = {
           "name": {"validators": []},
        }

class ArticleSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "identifier",
            "publication_date",
            "title",
            "abstract",
            "authors",
            "tags",
        ]

    def create(self, validated_data):
        authors_data = validated_data.pop("authors")
        tags_data = validated_data.pop("tags")
        article = Article.objects.create(**validated_data)

        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(name=author_data["name"])
            article.authors.add(author)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data["name"])
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        authors_data = validated_data.pop("authors", None)
        tags_data = validated_data.pop("tags", None)

        instance.identifier = validated_data.get("identifier", instance.identifier)
        instance.publication_date = validated_data.get("publication_date", instance.publication_date)
        instance.title = validated_data.get("title", instance.title)
        instance.abstract = validated_data.get("abstract", instance.abstract)
        instance.save()

        if authors_data is not None:
            instance.authors.clear()
            for author_data in authors_data:
                author, _ = Author.objects.get_or_create(name=author_data["name"])
                instance.authors.add(author)

        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                if "name" not in tag_data or not tag_data["name"]:
                    continue
                tag, _ = Tag.objects.get_or_create(name=tag_data["name"])
                instance.tags.add(tag)

        return instance

class CommentSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["id", "user", "created_at", "updated_at"]
