
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Topics, About, Article
from .serializers import ArticleDetailSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
