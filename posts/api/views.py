from rest_framework.generics import (
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView, 
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)

from ..models import Post
from .serializers import (
    PostCreateUpdateSerializer, 
    PostListSerializer, 
    PostDetailSerializer,
)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
