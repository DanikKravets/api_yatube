from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Group, Post, User


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    posts = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='posts',
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')


class PostSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'group', 'image')


class GroupSerializer(serializers.ModelSerializer):
    """Group model serializer."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'description', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    '''Comment model serializer.'''

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'post', 'created')
