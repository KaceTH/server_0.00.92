from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Post

class ReadPost(ModelSerializer) :

    category = serializers.IntegerField(source='format')
    content = serializers.CharField(source='text')
    user_id = serializers.StringRelatedField(source='author.username')
    user_name = serializers.StringRelatedField(source='author.name')
    grade_number = serializers.IntegerField(source='author.grade_number')

    class Meta:
        model = Post
        fields = [
            "create_at",
            "update_at",
            "user_id",
            "user_name",
            "grade_number",
            "id",
            "title",
            "category",
            "content",
        ]


class MakePost(ModelSerializer) :

    category = serializers.IntegerField(source='format')
    content = serializers.CharField(source='text')
    user_id = serializers.StringRelatedField(source='author.username')
    
    class Meta:
        model = Post
        fields = [
            "user_id",
            "title",
            "category",
            "content",
        ]


class EditPost(ModelSerializer) :

    content = serializers.CharField(source='text')

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
        ]