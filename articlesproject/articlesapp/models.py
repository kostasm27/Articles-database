from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    publication_date = models.DateField()
    authors = models.ManyToManyField(User, related_name="articles")
    abstract = models.TextField()
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.identifier})"


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.identifier}"
