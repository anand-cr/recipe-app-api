"""Serializer for Recipe"""


from django.db import models
from core.models import User, Recipe
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link')
        read_only_fields = ['id']


# NOTE9 : to create a recipe detail api
# create the serializer - extension of RecipeSerializer
# add an extra field description
# modify the recipeViewSet (check there for more info)
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
