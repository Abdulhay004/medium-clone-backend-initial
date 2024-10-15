import django_filters
from .models import ReadingHistory

class ReadingHistoryFilter(django_filters.FilterSet):
    class Meta:
        model = ReadingHistory
        fields = {
            'user': ['exact'],
            'article': ['exact'],
            'date_read': ['exact', 'gte', 'lte'],
        }