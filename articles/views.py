from array import array

from rest_framework import viewsets , status, mixins, generics, serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Topic, TopicFollow
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.http import Http404
from django.db import transaction

User = get_user_model()

from .filters import ArticleFilter

from users.models import Recommendation, ReadingHistory, Pin
from .models import Article, Comment, Favorite, Clap, Report
from .serializers import (ArticleCreateSerializer, ArticleDetailSerializer,
                          CommentSerializer, ArticleDetailCommentsSerializer,
                          ClapSerializer)


class ArticleDetailView(generics.RetrieveAPIView):
       queryset = Article.objects.all()
       serializer_class = ArticleDetailSerializer


class ArticlesView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter  # Set the filter class

    def post(self, request, id, action):
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response({"detail": "Maqola topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        if action == 'archive':
            article.archived = True  # Убедитесь, что у вас есть поле archived в модели Article
            article.save()
            return Response({"detail": "Maqola arxivlandi."}, status=status.HTTP_200_OK)
        elif action == 'pin':
            pin, created = Pin.objects.get_or_create(user=request.user, article=article)
            if created:
                return Response({"detail": "Maqola pin qilindi."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Maqola allaqachon pin qilingan."}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        try:
            article = Article.objects.get(id=id)
            pin = Pin.objects.get(user=request.user, article=article)
            pin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Pin.DoesNotExist:
            return Response({"detail": "Maqola topilmadi.."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        try:
            article = self.get_object()  # Get the article by ID
            article.reads_count += 1      # Increment reads count
            article.save()                 # Save the updated article

            # Optionally, add to user's reading history
            # ReadingHistory.objects.create(user=request.user, article=article)

            return Response({"detail": "Maqolani o'qish soni ortdi."}, status=status.HTTP_201_CREATED)
        except Article.DoesNotExist:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        try:
            article = self.get_object()
            article.views_count += 1
            article.save()
            ReadingHistory.objects.create(user=request.user, article=article)
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

class CreateCommentsView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        article_id = self.kwargs.get('id')
        if article_id:
            article = Article.objects.filter(id=article_id).first()
            if article and article.is_active and article.status != 'pending':
                return Article.objects.filter(id=article_id)
            else:
                raise Http404("No Article matches the given query.")
        return Article.objects.none()

    def perform_create(self, serializer):
        article1 = self.get_queryset().first()
        if not article1:
            raise Http404("Article not found or inactive.")
        else:
            serializer.save(article=article1, user=self.request.user)
        # Extract data from the request
        content = self.kwargs.get('content')
        parent_id = self.kwargs.get('parent_id')
        article_id = self.kwargs.get('article_id')

        # Check if the article exists
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"detail": "No Article matches the given query."}, status=status.HTTP_404_NOT_FOUND)

        # Check if content is provided
        if not content:
            return Response({"detail": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle parent comment if provided
        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                return Response({"detail": "Parent comment does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new comment
        comment = Comment.objects.create(content=content,
                                         author=self.request.user,
                                         article=article,
                                         parent=parent_comment)

        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            comment = self.get_object()  # Get the comment instance
        except Comment.DoesNotExist:
            return Response({"detail": "No Comment matches the given query."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the author of the comment
        if comment.user != request.user:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        # Use partial=True to allow partial updates
        serializer = self.get_serializer(comment, data=request.data, partial=True)

        # Validate the serializer data
        if serializer.is_valid():
            # Check if content is empty and raise a validation error if so
            if 'content' in serializer.validated_data and not serializer.validated_data['content']:
                return Response({"detail": "Content cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Save the updated comment
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
            if request.user != comment.user:
                return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
            self.perform_destroy(comment)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'detail': 'No Comment matches the given query.'},
                            status=status.HTTP_404_NOT_FOUND)
#
class ArticleDetailCommentsView(APIView):
    serializer_class = ArticleDetailCommentsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, article_id):
        try:
            # Fetch the article by ID
            article = Article.objects.get(id=article_id)
            # Fetch comments related to the article
            comments = Comment.objects.filter(article=article)
            # Serialize the comments
            serializer = CommentSerializer(comments, many=True)

            response_data = {
                "count": len(serializer.data),
                "next": None,
                "previous": None,
                "results": [{
                    "comments": serializer.data
                }]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response({'detail': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)

class FavoriteArticleView(APIView):
    queryset = Favorite.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter
    def post(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
            # Check if the article is already favorited
            if Favorite.objects.filter(user=request.user, article=article).exists():
                return Response({'detail': 'Maqola sevimlilarga allaqachon qo\'shilgan.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new favorite entry
            Favorite.objects.create(user=request.user, article=article)
            return Response({'detail': 'Maqola sevimlilarga qo\'shildi.'}, status=status.HTTP_201_CREATED)

        except Article.DoesNotExist:
            return Response({'detail': 'Maqola topilmadi.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
            favorite = Favorite.objects.filter(user=request.user, article=article)

            if not favorite.exists():
                return Response({'detail': 'Maqola sevimlilarga qo\'shilmagan.'}, status=status.HTTP_400_BAD_REQUEST)

            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Article.DoesNotExist:
            return Response({'detail': 'Maqola topilmadi.'}, status=status.HTTP_404_NOT_FOUND)

class ClapView(generics.GenericAPIView):
    serializer_class = ClapSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        article = Article.objects.get(id=article_id)
        clap, created = Clap.objects.get_or_create(user=request.user, article=article)

        if created:
            clap.count = 1
        else:
            if clap.count < 50:
                clap.count += 1


        clap.save()
        return Response(ClapSerializer(clap).data, status=status.HTTP_201_CREATED)

    def delete(self, request, article_id):
        # Delete all claps by the user for this article
        deleted_count, _ = Clap.objects.filter(user=request.user, article__id=article_id).delete()

        if deleted_count == 0:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

class ReportArticleView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        article_id = self.kwargs.get('id')
        user = request.user

        # Get the article
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"detail": "Maqola topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already reported this article
        if Report.objects.filter(article=article, user=user).exists():
            return Response({"detail": "Ushbu maqola allaqachon shikoyat qilingan."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new report and check report count
        with transaction.atomic():
            Report.objects.create(article=article, user=user)
            report_count = Report.objects.filter(article=article).count()

            # If report count exceeds 3, mark the article as trash
            if report_count >= 3:
                article.status = 'trash'
                article.save()
                return Response({"detail": "Maqola bir nechta shikoyatlar tufayli olib tashlandi."}, status=status.HTTP_200_OK)

        return Response({"detail": "Shikoyat yuborildi."}, status=status.HTTP_201_CREATED)