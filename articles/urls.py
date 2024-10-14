from django.urls import path, include
from rest_framework import routers
from .views import ArticlesView, TopicFollowView, CreateCommentsView


router = routers.SimpleRouter()
router.register('', ArticlesView)

urlpatterns = [
    # path('articles/<int:article_id>/detail/comments/', ArticleDetailCommentsView.as_view({'get': 'list'}), name='article-detail-comments'),
    # path('comments/<int:id>', CommentsView.as_view({'get': 'list'}), name='patch-delete-comment'),
    path('<int:id>/comments/', CreateCommentsView.as_view(), name='create-article-comments'),
    path('topics/<int:id>/follow/', TopicFollowView.as_view(), name='topic-follow'),
    path('', include(router.urls)),

]
