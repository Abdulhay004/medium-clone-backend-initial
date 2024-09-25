
from rest_framework import serializers
from .models import Topics, About, Author

class TopicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topics
        fields = "__all__"


class AboutSerializer(serializers.ModelSerializer):

    class Meta:
        model = About
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"



###I combine both Student and Course into one
class ArticleDetailSerializer(serializers.ModelSerializer):

    topics = serializers.SerializerMethodField()
    about = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_topics(self, obj):
        topics = obj.topics_set.all()
        serializer = TopicsSerializer(topics, many=True)
        return serializer.data

    def get_about(self, obj):
        about = obj.about_set.all()
        serializer = AboutSerializer(about, many=True, read_only=True)
        return serializer.data

    def get_author(self, obj):
        author = obj.author_set.all()
        serializer = AuthorSerializer(author, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Author
        fields = ('username','first_name','last_name', 'about', 'topic')