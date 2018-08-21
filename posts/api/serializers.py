from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from accounts.api.serializers import UserDetailSerializer
from ..models import Post


post_detail_url = HyperlinkedIdentityField(view_name='posts-api:detail', lookup_field='slug')


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            # 'id',
            'user',
            'title',
            # 'slug',
            'content',
            'publish',
        ]


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'title',
            'publish',
        ]


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    image = SerializerMethodField()
    html = SerializerMethodField()
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'user',
            'title',
            'slug',
            'content',
            'html',
            'publish',
            'image',
        ]

    def get_image(self, obj):
        try:
            return obj.image.url
        except:
            return None

    def get_html(self, obj):
        return obj.get_markdown()
