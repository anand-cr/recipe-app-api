"""Serializer for Recipe"""


from django.db import models
from core.models import User, Recipe, Tag
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

# create the tag serializer , add the view
#


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""
    # NOTE: Nested serializers
    # by default nested serializers are read only, add custom logic to make it writable
    # many=True implies this is a list
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link', 'tags')
        read_only_fields = ['id']

    def _get_or_create(self, recipe, tags):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    # Overrided cuz nested
    # Create here pops the tags
    # gets rest of the data from recipe
    # iterates through the tags {'name':'tag1'}, gets or creates and assigns them to the recipe model
    # returns the recipe,
    def create(self, validated_data):
        """Create a recipe"""
        # why pop? cuz the recipe
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        # why not self.request , because this is serializer and context is passed in by the view
        # https://detecttechnologies.udemy.com/course/django-python-advanced/learn/lecture/12712679#questions/10432054
        # ? auth_user = self.context['request'].user abstracted into _get_or_create() method
        # loop through tag from the pop
        # get_or_create() from model manager gets the value(tag) if it exists, else it will craete a new one
        # https://detecttechnologies.udemy.com/course/django-python-advanced/learn/lecture/32236986#questions/17881232
        # ?also abstracted into above method
        # for tag in tags:
        #     tag_obj, created = Tag.objects.get_or_create(
        #         user=auth_user,
        #         **tag,
        #     )
        #     recipe.tags.add(tag_obj)
        self._get_or_create(recipe, tags)

        return recipe

     # The `.update()` method does not support writable nested fields by default.
     # Write an explicit `.update()` method for serializer
     #

    def update(self, instance, validated_data):
        """Update recipe"""
        tags = validated_data.pop('tags', None)
        # ? auth_user = self.context['request'].user       abstracted
        if tags is not None:
            instance.tags.clear()
            self._get_or_create(instance, tags)
            # ? abstracted
            # for tag in tags:
            #     tag_obj, created = Tag.objects.get_or_create(
            #         user=auth_user,
            #         **tag)
            #     instance.tags.add(tag_obj)

        # rest of the data is set to the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# NOTE9 : to create a recipe detail api
# create the serializer - extension of RecipeSerializer
# add an extra field description
# modify the recipeViewSet (check there for more info)
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
