

from .models import Topic,Article
from django.shortcuts import get_object_or_404

from rest_framework import viewsets , status, mixins, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

User = get_user_model()

from .filters import ArticleFilter

from .models import Article
from .serializers import ArticleCreateSerializer, ArticleDetailSerializer, ArticleSerializer, AuthorSerializer, ArticleListSerializer


class ArticleDetailView(generics.RetrieveAPIView):
       queryset = Article.objects.all()
       serializer_class = ArticleDetailSerializer


class ArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter  # Set the filter class
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Article.DoesNotExist:
            return Response({'detail': 'No Article matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
    # def get_queryset(self):
    #     # Start with all articles
    #     queryset = Article.objects.all()
    #
    #     # Check if the 'get_top_articles' query parameter is in the request
    #     top_articles_count = self.request.query_params.get('get_top_articles', None)
    #
    #     if top_articles_count is not None:
    #         try:
    #             # Convert to an integer
    #             top_articles_count = int(top_articles_count)
    #             # Return the top 'n' articles, ordered by created_at (latest first)
    #             queryset = queryset.order_by('views_count')[:top_articles_count]
    #         except ValueError:
    #             pass  #
    #
    #     return queryset
