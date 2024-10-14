
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

class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
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
    class Meta:
        model = Comment
        fields = ['content']

    def create(self, validated_data):
        # Extract user from context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    # def get_replies(self, obj):
    #     return CommentSerializer(obj.replies.all(), many=True).data
class ArticleDetailCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'parent', 'content', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at', 'user']

    def get_replies(self, obj):
        # Fetch replies for the comment
        replies = Comment.objects.filter(parent=obj)
        return ArticleDetailCommentsSerializer(replies, many=True).data



