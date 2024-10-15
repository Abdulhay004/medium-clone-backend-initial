import django_filters
from django.db.models import Q
from .models import Article
from users.models import Recommendation
from django_filters import rest_framework as filters

class ArticleFilter(django_filters.FilterSet):
    is_user_favorites = filters.BooleanFilter(field_name='favorites__is_favorite', method='filter_favorites')
    get_top_articles = django_filters.NumberFilter(method='filter_get_top_articles')
    topic_id = filters.NumberFilter(field_name='topics__id', lookup_expr='exact')
    is_recommended = filters.BooleanFilter(field_name='is_recommend', label='Is Recommended')
    search = filters.CharFilter(method='filter_by_search')
    class Meta:
        model = Article
        fields = ['topic_id', 'is_recommended', 'is_user_favorites']

    def filter_favorites(self, queryset, name, value):
        user = self.request.user  # Get the current user
        if user.is_authenticated:
            if value:
                # Filter articles that are marked as favorites by the user
                return queryset.filter(favorites__user=user)
            else:
                # If not favorited, exclude those articles
                return queryset.exclude(favorites__user=user)
        return queryset  # If user is not authenticated, return full queryset

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(topics__name__icontains=value) |
            Q(title__icontains=value) |
            Q(summary__icontains=value) |
            Q(content__icontains=value)
        ).distinct()
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




