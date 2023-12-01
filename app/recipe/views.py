"""
Views for the recipe API
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiTypes,)

from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient
)
from recipe import serializers


@extend_schema_view(
    list=extend_schema(
        description='List all recipes for the authenticated user',
        parameters=[
            OpenApiParameter(
                name='tags',
                description='Filter recipes by tags',
                required=False,
                type=str,
                location='query',
                examples=[
                    OpenApiExample(
                        name='List recipes with tag 1 and 2',
                        value='1,2'
                    )
                ]
            ),
            OpenApiParameter(
                name='ingredients',
                description='Filter recipes by ingredients',
                required=False,
                type=str,
                location='query',
                examples=[
                    OpenApiExample(
                        name='List recipes with ingredient 1 and 2',
                        value='1,2'
                    )
                ]
            )
        ]
    ),
)
class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeDetailSerializer
    # The authentication class is a list because we can have multiple
    # authentication classes.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        # The map function takes a function and an iterable.
        # It applies the function to each element of the iterable.
        # The map function returns a map object.
        # We can convert the map object to a list.
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # The double underscores allow us to filter on a field
            # of a related model.
            # We can also filter on multiple fields of a related model.
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            # The double underscores allow us to filter on a field
            # of a related model.
            # We can also filter on multiple fields of a related model.
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # The action attribute is set by the viewset.
        # It tells us what action is being performed.
        # This allows us to use different serializers for different actions.
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # The serializer will take care of adding the user to the data.
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # The pk is the primary key of the recipe that we want to upload
        # the image to.
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema_view(
    list=extend_schema(
        description='List all tags for the authenticated user',
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes',
            )
        ]
    ),
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # The request object has a user object attached to it.
        # We can use this to filter the queryset.
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            # The double underscores allow us to filter on a field
            # of a related model.
            # We can also filter on multiple fields of a related model.
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all().order_by('-name')


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all().order_by('-name')
