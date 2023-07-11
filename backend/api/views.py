from api.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)
from django.db.models import F, Sum
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('head', 'options', 'get', 'post', 'patch', 'delete')

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        queryset = ShoppingCart.objects.filter(
            user=request.user
        ).values(
            name=F("recipe__ingredients__ingredient__name")
        ).annotate(
            amount=Sum("recipe__ingredients__amount")
        )
        return Response(queryset)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        serializer = ShoppingCartSerializer(
            data={"recipe": pk}, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            if request.method == "POST":
                serializer.save()
                return Response(serializer.data)

            ShoppingCart.objects.get(user=request.user, recipe_id=pk).delete()
            return Response(status=204)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        serializer = FavoriteSerializer(
            data={"recipe": pk}, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            if request.method == "POST":
                serializer.save()
                return Response(serializer.data)

            Favorite.objects.get(user=request.user, recipe_id=pk).delete()
            return Response(status=204)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()