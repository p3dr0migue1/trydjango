from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

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
    user = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'content',
            'publish',
        ]

    def get_user(self, obj):
        return obj.user.username


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()

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

    def get_user(self, obj):
        return obj.user.username

    def get_image(self, obj):
        try:
            return obj.image.url
        except:
            return None

    def get_html(self, obj):
        return obj.get_markdown()
