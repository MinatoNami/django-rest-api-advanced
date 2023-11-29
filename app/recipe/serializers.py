"""
Serializers for recipe app
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'description',
            'time_minutes',
            'price',
            'link'
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail objects"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields = ('description')
        # read_only_fields = RecipeSerializer.Meta.read_only_fields