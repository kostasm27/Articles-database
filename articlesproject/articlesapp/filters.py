import django_filters
from .models import Article


class ArticleFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(
        field_name="publication_date", lookup_expr="year"
    )
    month = django_filters.NumberFilter(
        field_name="publication_date", lookup_expr="month"
    )
    authors = django_filters.AllValuesMultipleFilter(field_name="authors")
    tags = django_filters.CharFilter(method="filter_by_tags")

    def filter_by_tags(self, queryset, name, keyword):
        """
        Filters tags to find possible matches based on keyword
        """
        return queryset.filter(tags__icontains=keyword)

    class Meta:
        model = Article
        fields = ["year", "month", "authors", "tags"]
