from django.shortcuts import render

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from core import models

from user.serializers import UserSerializer, AuthTokenSerializer

# NOTE: viewset vs APIView -> DRF baseclasses
# APIView -> Focused on HTTP methods , more flexible, (GET POST PUT PATCH DELETE)
# Useful for non CRUD APIs
# great for auth,jobs,external apis (ie, anything taht doest map to specific models)

# Viewset -> focused around action (Retrive,list,update,partial update, destroy)
# Maps to Django models
# routers generate urls
# great for crud operations


# Create your views here.


# why generics->https://detecttechnologies.udemy.com/course/django-python-advanced/learn/lecture/12712679#questions/7659030
# CreateAPIView This is a "generic" class for adding a POST handler for building API's which create objects.
class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    serializer_class = UserSerializer
    # queryset = models.User.objects.all()

# the default ObtainAuthToken uses username and password so we override by giving our own serializer class
# The data


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # https://detecttechnologies.udemy.com/course/django-python-advanced/learn/lecture/12712663#questions/6637606
    # ObtainAuthToken does not implement browsable api (/token/ page wont work) so we manually add it
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# RetrieveUpdateAPIView is inbuilt api view to retrieve(get) and update(PATCH)
# set the serializer class
# Use token_authentication for authentication (is the person who they ay they are)
# permission : if they are authenticated they can use the api
# OVERRIDE the get_object method
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # we overide this to make sure when we make a get request we retrive the authenticated user and run it through the serializer
    def get_object(self):
        """Return the user object for the current authenticated user"""
        return self.request.user
