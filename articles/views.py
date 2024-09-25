
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Topics, About, Article
from .serializers import ArticleDetailSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Topics.objects.all()
    serializer_class = ArticleDetailSerializer
    def create(self, request, pk=None):
       serializer = self.get_serializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       self.perform_create(serializer)
       headers = self.get_success_headers(serializer.data)
       author_id  = serializer.data['id']
       name = serializer.data['Name']
       return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)