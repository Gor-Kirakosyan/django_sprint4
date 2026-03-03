from rest_framework import serializers
from posts.models import Comment, Post, Follow
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', 
        read_only=True
    )
    
    class Meta:
        fields = '__all__'
        model = Post

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, 
        slug_field='username'
    )
    
    class Meta:
        fields = '__all__'
        model = Comment

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value