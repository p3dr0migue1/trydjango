from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
)

from ..models import Comment


User = get_user_model()


def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp',
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.user = user
            self.parent_obj = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)

                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super().__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)

            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")

            # provides reference to the Post Model
            post_model = model_qs.first().model_class()
            # equivalent to --> Post.objects.filter(slug=self.slug)
            obj_qs = post_model.objects.filter(slug=self.slug)

            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")

            if self.user is None:
                user = User.objects.all().first()
            else:
                user = self.user

            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type,
                slug,
                content,
                user,
                parent_obj=parent_obj,
            )
            return comment
    return CommentCreateSerializer


class CommentListSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    url = HyperlinkedIdentityField(view_name='comments-api:detail')

    class Meta:
        model = Comment
        fields = [
            'id',
            'url',
            'content',
            'reply_count',
            'timestamp',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]


class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'replies',
            'reply_count',
            'content_object_url',
            'timestamp',
        ]

        read_only_fields = [
            # 'content_type',
            # 'object_id',
            'reply_count',
            'replies',
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None
