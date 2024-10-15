
from rest_framework import serializers, generics
from .models import Topic, Article, Clap, User, Author, Comment

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
           model = Topic
           fields = ['id', 'title', 'description']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author  # Ensure this is the correct model
        fields = ['id', 'name', 'title']




###I combine both Student and Course into one
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Article


class ArticleCreateSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    topic_ids = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(),
        many=True,
        write_only=True
    )

    topics = TopicSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'summary', 'content', 'thumbnail', 'topics', 'topic_ids', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
            topic_ids = validated_data.pop('topic_ids', [])
            if not isinstance(topic_ids, list):
                topic_ids = [topic_ids]
            request = self.context.get('request')
            author = request.user
            article = Article.objects.create(author=author, **validated_data)
            article.topics.set(topic_ids)
            return article

    def update(self, instance, validated_data):
        # Bu yerda tags ni olish va yangilashni amalga oshirish
        tags = validated_data.pop('tags', [])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        # Tags ni yangilash
        if tags:
            instance.tags.clear()
            instance.tags.add(*tags)

        return instance





class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'middle_name', 'email', 'avatar']
class CommentSerializer(serializers.ModelSerializer):
    article = serializers.IntegerField(source='article.id', read_only=True)
    class Meta:
        model = Comment
        fields = ['parent', 'content', 'article']

class ArticleDetailCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    replies = serializers.ListField(child=serializers.DictField(), default=[])

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'parent', 'content', 'created_at', 'replies']

class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = ['user', 'article', 'count']



