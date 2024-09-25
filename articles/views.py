
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Topic, About, Article
from .serializers import ArticleDetailSerializer

class ArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
