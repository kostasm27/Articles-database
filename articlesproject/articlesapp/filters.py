import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="publication_date", lookup_expr="year")
    month = django_filters.NumberFilter(field_name="publication_date", lookup_expr="month")
    authors = django_filters.CharFilter(method="filter_authors")
    tags = django_filters.CharFilter(method="filter_tags")

    def filter_authors(self, queryset, name, value):
        """
        Filters authors to find possible matches
        """
        return queryset.filter(authors__name__icontains=value)

    def filter_tags(self, queryset, name, value):
        """
        Filters tags to find possible matches
        """
        return queryset.filter(tags__name__icontains=value)

    class Meta:
        model = Article
        fields = ["year", "month", "authors", "tags"]
