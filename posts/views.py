from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True)
    def like(self, request, pk):
        post = self.get_object()
        post.likes.add(request.user)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True)
    def unlike(self, request, pk):
        post = self.get_object()
        post.likes.remove(request.user)

        return Response(status=status.HTTP_200_OK)
