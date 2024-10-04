import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    get_top_articles = django_filters.NumberFilter(method='filter_get_top_articles')
    topic_id = django_filters.NumberFilter(field_name='topic_id')
    class Meta:
        model = Article
        fields = ['topic_id']  # We can leave this empty for custom filtering

    def filter_get_top_articles(self, queryset, name, value):
        if value:
            try:
                top_count = int(value)
                return queryset.order_by('-views_count')[:top_count]
            except ValueError:
                return queryset  # Invalid value, return unfiltered queryset
        return queryset  # If no value is provided, return unfiltered queryset Less than
