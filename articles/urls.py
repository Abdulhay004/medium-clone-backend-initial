from django.urls import path, include
from rest_framework import routers
from .views import ArticlesView, ArticleDetailView


router = routers.SimpleRouter()
router.register('', ArticlesView)

urlpatterns = [
    # path('', ArticleCreateView.as_view(), name='article-create'),
    path('', include(router.urls))
]
