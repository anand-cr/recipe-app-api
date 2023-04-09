""" serializer"""

from django.db import models
from core.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

# https://detecttechnologies.udemy.com/course/django-python-advanced/learn/lecture/32237146#questions/7638536

# NOTE4: To Make serializer and use the view to display using modelserializer baseclass
# fill  the  model fields extra_kwargs
# define the create method which overrides the default create method of serializer
# Create the CreateUserView
# Hook it up on the urlpatterns /create and then add to the main urls file


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {'input_type': 'password'}
            }
        }
    # Overrides serializer default behaviour, if we pass in password it will be passed in as clear test
    # so we use create_user which encrypts the data
    # this create function will be called after the validation, with validated data from serializer

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    # NOTE7: to update the user
    # create update method
    # the reason why we are overriding it is because the default update method stores password in clear text
    # only we set the password ourself we can use the inbuilt update method to update the rest
    # return the user to the view

    def update(self, instance, validated_data):
        """Update and return the user instance"""
        password = validated_data.pop(
            'password', None)  # pass is optional so if user dont provide password just default it to None
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


# NOTE6 - creating the token
# when username(email in this case) is given we generate a token
# AuthTokenSerializer takes in email and password from the  view(/api/users/token) -> validate it and generates the token
# CreateTokenView is the graphical interface for it
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # when the data is passed to the view , it will pass to the serializer to validate
    # retrive
    def validate(self, attrs):
        """validate and authenticate the users"""
        email = attrs.get('email')
        password = attrs.get('password')

        # inbuilt authentication system , it will check if username and password is correct
        # if yes it will return user else empty
        user = authenticate(
            # no purppose but required field
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _("unaable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        # ???
        attrs['user'] = user
        return attrs
