
from rest_framework import serializers
from .models import Topic, Article, Clap, User

class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = "__all__"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'is_active']

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = "__all__"



###I combine both Student and Course into one
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Article



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
