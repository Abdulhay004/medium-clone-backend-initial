

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

from users.models import Recommendation
from .models import Article
from .serializers import ArticleCreateSerializer, ArticleDetailSerializer, ArticleSerializer, AuthorSerializer, ArticleListSerializer


class ArticleDetailView(generics.RetrieveAPIView):
       queryset = Article.objects.all()
       serializer_class = ArticleDetailSerializer


class ArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter  # Set the filter class
    def destroy(self, request, *args, **kwargs):
        # Get the article instance
        article = self.get_object()

        # Check if the user is the author of the article
        if article.author != request.user:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        # Set the article's status to TRASH
        article.status = 'TRASH'
        article.save()

        return Response({"message": "Article moved to trash."}, status=status.HTTP_204_NO_CONTENT)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Article.DoesNotExist:
            return Response({'detail': 'No Article matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        is_recommend = self.request.query_params.get('is_recommend', None)
        if is_recommend and self.request.user.is_authenticated:
            user_recommendations = Recommendation.objects.get(user=self.request.user)
            recommended_articles_ids = user_recommendations.more_recommend.values_list('id', flat=True)
            return Article.objects.filter(id__in=recommended_articles_ids)
        return Article.objects.all()


