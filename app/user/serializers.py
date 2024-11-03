"""
Serializers for the user API view.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,                           # To use Django's authentication framework
)

from django.utils.translation import gettext as _  #Allow translations

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):  #ModelSerializer allows to automatically apply info to the Model
    """Serializer for the user object"""

    class Meta:  #Specifies what information (fields, kwargs, etc) we will pass/made available to the serializer
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Override create method so that we return a user with encrypted password. Only called after
        validation and if there is no validation error. If it fails returns a 400 response code"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):  # instance = model item that is being updated.
        """Update and return user"""
        password = validated_data.pop('password', None) #retrieve and remove the password from the dictionary
        user = super().update(instance, validated_data) #super to call UserSerialializer update method and only changing what's required

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()            # allows secure password field in api testing
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user. This method is called on the validation stage
        by the relevant view"""
        email = attrs.get('email')              # Gets attributed passed on the
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
