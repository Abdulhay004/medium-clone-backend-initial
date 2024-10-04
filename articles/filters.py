import django_filters
from .models import Article
from django_filters import rest_framework as filters

class ArticleFilter(django_filters.FilterSet):
    get_top_articles = django_filters.NumberFilter(method='filter_get_top_articles')
    topic_id = filters.NumberFilter(field_name='topics__id', lookup_expr='exact')
    def filter_get_top_articles(self, queryset, name, value):
            if value:
                try:
                    top_count = int(value)
                    return queryset.order_by('-views_count')[:top_count]
                except ValueError:
                    return queryset  # Invalid value, return unfiltered queryset
            return queryset

    class Meta:
        model = Article
        fields = ['topic_id']

