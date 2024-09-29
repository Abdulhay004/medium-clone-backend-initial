from django.urls import path, include
from rest_framework import routers
from .views import ArticlesView, ArticleDetailView

router = routers.SimpleRouter()
router.register('', ArticlesView)

urlpatterns = [
    # path('', ArticlesView.as_view({'get': 'list'}), name='article-list'),
    # path('<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('', include(router.urls)),
]
