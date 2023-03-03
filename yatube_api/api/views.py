from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post, User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """User model view set."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Group model view set."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Post model view set."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        """Create new post with author."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Update post with author."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('You can not update this post')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        """Delete post with author."""
        if instance.author != self.request.user:
            raise PermissionDenied('You can not delete this post')
        super(PostViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    """Comment model view set."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        """Get comments for post."""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        """Create new comment with author."""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Update comment with author."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('You can not update this comment')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        """Delete comment with author."""
        if instance.author != self.request.user:
            raise PermissionDenied('You can not delete this comment')
        super(CommentViewSet, self).perform_destroy(instance)
