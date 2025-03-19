from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    publication_date = models.DateField()
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    authors = models.ManyToManyField(Author, related_name="articles")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_articles")
    tags = models.ManyToManyField(Tag, related_name="articles")

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.identifier}"
