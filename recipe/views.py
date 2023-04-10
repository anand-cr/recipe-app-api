# from django.shortcuts import render
# from rest_framework import generics, authentication, permissions
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.settings import api_settings
#
from core.models import Recipe
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe.serializers import RecipeSerializer

# Create your views here.

# to use


class RecipeViewSet(viewsets.ViewSet):
    """Manage recipe """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # override
    # typicallu we return all of the objects
    # here we are filtering for the specific user(we already know they are authenticated cuz of the authenticated_classes)
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
