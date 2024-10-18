from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from catalog.api.serializers import ProductSerializer, CategorySerializer
from catalog.models import Product, Category

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).language(self.request.query_params.get('lang', 'uz')).all()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.filter(is_active=True).language(self.request.query_params.get('lang', 'uz')).all()

    def retrieve(self, request, slug=None):
        category = self.get_object()
        products = Product.objects.filter(category=category, is_active=True).language(request.query_params.get('lang', 'uz'))
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

