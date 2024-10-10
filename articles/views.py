
from rest_framework import viewsets , status, mixins, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter  # Set the filter class


    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        if request.user == article.author:
            article.status = 'trash'
            article.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            article = self.get_object()
            if article.status == 'trash':
                return Response(status=status.HTTP_404_NOT_FOUND)
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


