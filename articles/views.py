
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Topic, About, Article
from .serializers import ArticleCreateSerializer

class ArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = ArticleCreateSerializer(date=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
