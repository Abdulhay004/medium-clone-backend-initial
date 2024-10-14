
from rest_framework import viewsets , status, mixins, generics, serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Topic, TopicFollow
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F

User = get_user_model()

from .filters import ArticleFilter

from users.models import Recommendation
from .models import Article, Comment
from .serializers import ArticleCreateSerializer, ArticleDetailSerializer, CommentSerializer, ArticleDetailCommentsSerializer


class ArticleDetailView(generics.RetrieveAPIView):
       queryset = Article.objects.all()
       serializer_class = ArticleDetailSerializer


class ArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter  # Set the filter class

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        summary = request.data.get('summary')
        if summary:
            instance.summary = summary

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        if request.user == article.author:
            article.status = 'trash'
            article.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        is_recommend = self.request.query_params.get('is_recommend', None)
        if is_recommend and self.request.user.is_authenticated:
            user_recommendations = Recommendation.objects.get(user=self.request.user)
            recommended_articles_ids = user_recommendations.more_recommend.values_list('id', flat=True)
            return Article.objects.filter(id__in=recommended_articles_ids)
        return Article.objects.all()


class TopicFollowView(APIView):
    def post(self, request, id):
        try:
            topic = Topic.objects.get(id=id)
        except Topic.DoesNotExist:
            return Response({"detail": "Hech qanday mavzu berilgan soʻrovga mos kelmaydi."}, status=status.HTTP_404_NOT_FOUND)

        if TopicFollow.objects.filter(user=request.user, topic=topic).exists():
            return Response({"detail": f"Siz allaqachon '{topic.name}' mavzusini kuzatyapsiz."}, status=status.HTTP_200_OK)

        TopicFollow.objects.create(user=request.user, topic=topic)
        return Response({"detail": f"Siz '{topic.name}' mavzusini kuzatyapsiz."}, status=status.HTTP_201_CREATED)
    def delete(self, request, id):
        try:
            topic = Topic.objects.get(id=id)
        except Topic.DoesNotExist:
            return Response({"detail": "Hech qanday mavzu berilgan soʻrovga mos kelmaydi."}, status=status.HTTP_404_NOT_FOUND)

        try:
            follow_instance = TopicFollow.objects.get(user=request.user, topic=topic)
            follow_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TopicFollow.DoesNotExist:
            return Response({"detail": f"Siz '{topic.name}' mavzusini kuzatmaysiz."}, status=status.HTTP_404_NOT_FOUND)

create_comments_data = [
        ("valid_data", 201),
        ("invalid_data", 400),
        ("article_status_inactive", 403),
        ("empty_content", 400),
        ("required_content", 201),
        ("non_existent_article_id", 404)
    ]
from django.http import Http404

class CreateCommentsView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        article_id = self.kwargs.get('id')
        if article_id:
            article = Article.objects.filter(id=article_id).first()
            if article and article.is_active:
                return Article.objects.filter(id=article_id)
            else:
                raise Http404("Article not found or inactive.")
        return Article.objects.none()

    def perform_create(self, serializer):
        article_id = self.kwargs['id']
        article = self.get_queryset().first()
        if not article:
            raise Http404("Article not found or inactive.")

        serializer.save(article=article, user=self.request.user)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# class CommentsView(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_update(self, serializer):
#         serializer.save()
#
#     def perform_destroy(self, instance):
#         instance.delete()
#
# class ArticleDetailCommentsView(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#
#     def list(self, request, article_id=None):
#         queryset = Comment.objects.filter(article_id=article_id, parent=None)  # Top-level comments only
#         serializer = ArticleDetailCommentsSerializer(queryset, many=True)
#
#         return Response({
#             "count": len(serializer.data),
#             "next": None,
#             "previous": None,
#             "results": [{
#                 "comments": serializer.data
#             }]
#         })