import django_filters
from django.db.models import Q
from .models import Article
from users.models import Recommendation
from django_filters import rest_framework as filters

class ArticleFilter(django_filters.FilterSet):
    get_top_articles = django_filters.NumberFilter(method='filter_get_top_articles')
    topic_id = filters.NumberFilter(field_name='topics__id', lookup_expr='exact')
    is_recommended = filters.BooleanFilter(field_name='is_recommend', label='Is Recommended')
    def filter_get_top_articles(self, queryset, name, value):
            if value:
                try:
                    top_count = int(value)
                    return queryset.order_by('-views_count')[:top_count]
                except ValueError:
                    return queryset  # Invalid value, return unfiltered queryset
            return queryset
    def filter_by_recommend(self, queryset, name, value):
        user = self.request.user
        recommendations = Recommendation.objects.filter(user=user)
        more_topics = recommendations.values_list('more', flat=True)
        less_topics = recommendations.values_list('less', flat=True)


        if more_topics.exists():
            queryset = queryset.filter(Q(topics__in=more_topics))

        if less_topics.exists():
            queryset = queryset.exclude(topics__in=less_topics)

        return queryset

    class Meta:
        model = Article
        fields = ['topic_id', 'is_recommended']



