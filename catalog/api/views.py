from django.db.models import Q, Case, When, Value, IntegerField, Subquery, OuterRef
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from catalog.api.serializers import ProductSerializer, CategorySerializer, ManufacturerSerializer
from catalog.models import Product, Category, Manufacturer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = "slug"

    def get_queryset(self):
        lang = self.request.query_params.get("lang", "uz")
        search_query = self.request.query_params.get("search")
        manufactures_query = self.request.query_params.get("manufactures")
        category_query = self.request.query_params.get("category")
        
        # Базовый фильтр для активных продуктов с выбором языка
        queryset = Product.objects.filter(is_active=True).language(lang)

        # Применение поиска с аннотацией по релевантности
        if search_query:
            queryset = queryset.filter(
                Q(translations__name__icontains=search_query) | 
                Q(translations__description__icontains=search_query)
            ).annotate(
                relevance=(
                    Case(
                        When(translations__name__icontains=search_query, then=Value(2)),
                        When(translations__description__icontains=search_query, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                )
            ).order_by("-relevance")

        # Фильтр по производителям и категориям, если указаны
        if manufactures_query:
            queryset = queryset.filter(manufactures__translations__name=manufactures_query)
        if category_query:
            queryset = queryset.filter(category__slug=category_query)

        # Удаление дубликатов и возвращение итогового запроса
        return queryset.distinct()

    def get_object(self):
        # Поиск конкретного продукта по slug с языковым фильтром
        product = Product.objects.filter(
            slug=self.kwargs["slug"], 
            is_active=True
        ).language(self.request.query_params.get("lang", "uz")).first()
        
        if not product:
            raise NotFound("Product not found")
        return product


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    lookup_field = "slug"

    def get_queryset(self):
        lang = self.request.query_params.get("lang", "uz")
        queryset = Category.objects.language(lang)
        return queryset


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = "name"
    pagination_class = None

    def get_queryset(self):
        lang = self.request.query_params.get("lang", "uz")
        search_query = self.request.query_params.get("category")

        # Фильтруем по языку, если у вас есть такое поле в модели
        queryset = Manufacturer.objects.language(lang)

        if search_query:
            # Фильтрация по категории продукта, если у вас правильно настроена связь
            queryset = queryset.filter(
                product__category__slug=search_query
            ).distinct()
        
        return queryset

