from django.urls import path, include
from rest_framework import routers
from .views import ArticlesView, TopicFollowView


router = routers.SimpleRouter()
router.register('', ArticlesView)

urlpatterns = [
    path('topics/<int:id>/follow/', TopicFollowView.as_view(), name='topic-follow'),
    path('', include(router.urls)),

]
