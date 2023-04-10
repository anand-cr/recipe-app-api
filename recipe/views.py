"""Recipe view"""

# from django.shortcuts import render
# from rest_framework import generics, authentication, permissions
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.settings import api_settings
#
from core.models import Recipe
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers

# Create your views here.

# to use
# admintest@example.com
# pass123*


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipe """
    # serializer_class = serializers.RecipeSerializer
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # override
    # typically we return all of the objects
    # here we are filtering for the specific user(we already know they are authenticated cuz of the authenticated_classes)
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # overide so we canfigure the serializer class based on action
    # set the default serializer as the RecipeDeatilSerializer (we use it a lot more)
    # if teh action is listing then we use recipeserialzier else use teh deafult serialiser class we set
    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    # NOTE10: override
    # when we perform the creation of a new recipe through this viewset,we call this method,
    # when we save we will save the user value to the current authenticated user(performed by serializer)
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
