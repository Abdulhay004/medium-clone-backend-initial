

from .models import Topic,Article
from django.shortcuts import get_object_or_404

from rest_framework import viewsets , status, mixins, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Article
from .serializers import ArticleCreateSerializer, ArticleDetailSerializer, ArticleSerializer, AuthorSerializer


class ArticleDetailView(generics.RetrieveAPIView):
       queryset = Article.objects.all()
       serializer_class = ArticleDetailSerializer


class ArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Article.DoesNotExist:
            return Response({'detail': 'No Article matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
