""""
Serializers for recipe API.
"""

from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe."""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_in_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe Details. """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']