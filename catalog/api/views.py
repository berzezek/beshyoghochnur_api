from rest_framework import viewsets

from catalog.api.serializers import ProductSerializer, CategorySerializer
from catalog.models import Product, Category


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
