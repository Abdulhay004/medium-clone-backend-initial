
from rest_framework import serializers
from .models import Topic, About, Article

class TopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = "__all__"


class AboutSerializer(serializers.ModelSerializer):

    class Meta:
        model = About
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = "__all__"



###I combine both Student and Course into one
class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'