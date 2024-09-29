
from rest_framework import serializers
from .models import Topic, About, Article, Clap

class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = "__all__"
class TopicSerializer(serializers.ModelSerializer):

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
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

from .models import Article


User = get_user_model()

# class AuthorSerializer(serializers.ModelSerializer):
#     following = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def get_following(self, obj):
#         user = self.context.get('request').user
#         if user.is_authenticated:
#             return obj.followers.filter(pk=user.id).exists()
#         return False


class ArticleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'title', 'summary', 'content', 'topic_ids', 'created_at']
    def create(self, validated_data):
        article = Article(
            author=self.context['request'].user,
            **validated_data
        )
        article.save()
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        instance.tags.clear()
        instance.tags.add(*tags)

        return instance





class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = '__all__'
