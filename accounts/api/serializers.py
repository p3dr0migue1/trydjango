from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)


User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    # make email field required
    email = EmailField(label="Email Address")
    email2 = EmailField(label="Confirm Email")

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    # def validate(self, data):
    #     email = data['email']
    #     user = User.objects.filter(email=email)
    #     if user.exists():
    #         raise ValidationError("This email is already registered.")
    #     return data

    def validate_email(self, value):
        email = value
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError("This email is already registered.")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_object = User(
            username=username,
            email=email,
        )
        user_object.set_password(password)
        user_object.save()
        return validated_data


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserLoginSerializer(ModelSerializer):
    # make email field required
    email = EmailField(label="Email Address", required=False, allow_blank=True)
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        username = data.get('username', None)
        if not email and not username:
            raise ValidationError("Username or Email is required to login.")

        # get user by either email or username
        user = User.objects.filter(Q(email=email) | Q(username=username)).distinct()
        if user.exists and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("Username or Email is invalid.")
        
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Username/Email or Passwor are incorrect")
        data['token'] = "Some RANDOM T0k3n"  
        return data

