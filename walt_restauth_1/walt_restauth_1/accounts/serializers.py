from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)

    def validate_email(self, value):
        users = self.context['view'].get_users_by_email(value)
        if not users.exists():
            self.fail('email_not_found')
        else:
            return value

class CustomUserCreateSerializer(serializers.ModelSerializer):
    roles = serializers.ChoiceField(choices=CustomUser.ROLES)
    # email = serializers.EmailField(required=True) # Update: made email field required

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            roles=validated_data['roles'] # Added for 'roles'
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate_email(self,value):
        try:
            CustomUser.objects.get(email=value)
            raise serializers.ValidationError('This email is already in use.')
        except ObjectDoesNotExist:
            return value

    def validate(self, data):
        if 'password' not in data:
            raise serializers.ValidationError("Password field is required")
        return data

    def get_roles(self, obj):
        return getattr(obj, 'roles', None)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'roles',
        ]
        read_only_fields = ['roles']

class TokenObtainPairSerializer(TokenObtainSerializer):
    default_error_messages = {
        'no_account': _('No account found with the given credentials'),
        'not_active': _('Non-active account found')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
            'ip': self.context['request'].META['HTTP_CF_CONNECTING_IP']
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_account'],
                'invalid-credentials',
            )
        if not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['not_active'],
                'not-active',
            )

        data = {}

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access)
        return data
