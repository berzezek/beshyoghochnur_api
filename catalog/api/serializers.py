from rest_framework import serializers
from catalog.models import Category, Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('url', 'name', 'slug', 'description', 'price', 'image')
        extra_kwargs = {
            'url': {'view_name': 'product-detail', 'lookup_field': 'slug'}
        }

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'name', 'image', 'slug')
        extra_kwargs = {
            'url': {'view_name': 'category-detail', 'lookup_field': 'slug'}
        }
