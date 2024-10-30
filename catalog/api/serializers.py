from rest_framework import serializers
from catalog.models import Category, Product, Manufacturer

from rest_framework import serializers
from catalog.models import Product


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'name', 'image', 'slug')
        extra_kwargs = {
            'url': {'view_name': 'category-detail', 'lookup_field': 'slug'}
        }

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('url', 'name')
        extra_kwargs = {
            'url': {'view_name': 'manufacturer-detail', 'lookup_field': 'name'}
        }

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SerializerMethodField()
    manufactures = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('url', 'name', 'category', 'manufactures', 'slug', 'description', 'price', 'image')
        extra_kwargs = {
            'url': {'view_name': 'product-detail', 'lookup_field': 'slug'}
        }


    def get_category(self, obj):
        return obj.category.safe_translation_getter('name', any_language=True) if obj.category else None

    def get_manufactures(self, obj):
        return obj.manufactures.safe_translation_getter('name', any_language=True) if obj.manufactures else None