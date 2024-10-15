from django.urls import path, include
from rest_framework import routers
from .views import (ArticlesView, TopicFollowView,
                    CreateCommentsView, CommentsView,
                    ArticleDetailCommentsView,
                    FavoriteArticleView, ClapView)


router = routers.SimpleRouter()
router2 = routers.SimpleRouter()
router.register('', ArticlesView)
router2.register('comments', CommentsView)

urlpatterns = [
    path('<int:article_id>/clap/', ClapView.as_view(), name='clap'),
    path('<int:article_id>/favorite/', FavoriteArticleView.as_view(), name='favorite-article'),
    path('<int:article_id>/detail/comments/', ArticleDetailCommentsView.as_view(), name='article-detail-comments'),
    path('<int:id>/comments/', CreateCommentsView.as_view(), name='create-article-comments'),
    path('topics/<int:id>/follow/', TopicFollowView.as_view(), name='topic-follow'),
    path('', include(router.urls)),
    path('', include(router2.urls))

]
