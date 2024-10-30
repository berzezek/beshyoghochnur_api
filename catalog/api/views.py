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
        search_query = self.request.query_params.get("search", "")
        manufactures_query = self.request.query_params.get("manufactures", "")
        category_query = self.request.query_params.get("category", "")
        
        queryset = Product.objects.filter(is_active=True).language(lang)

        if search_query:
            queryset = (
                queryset.filter(
                    Q(translations__name__icontains=search_query) |
                    Q(translations__description__icontains=search_query)
                )
                .annotate(
                    relevance=(
                        Case(
                            When(translations__name__icontains=search_query, then=Value(2)),
                            default=Value(0),
                            output_field=IntegerField(),
                        ) +
                        Case(
                            When(translations__description__icontains=search_query, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField(),
                        )
                    )
                )
                .order_by("-relevance")
            )

        if manufactures_query:
            queryset = queryset.filter(manufactures__translations__name=manufactures_query)

        if category_query:
            queryset = queryset.filter(category__slug=category_query)

        # Удаление дубликатов
        return queryset.distinct()

    def get_object(self):
        product = (
            Product.objects.filter(slug=self.kwargs["slug"], is_active=True)
            .language(self.request.query_params.get("lang", "uz"))
            .first()
        )
        if not product:
            raise NotFound("Product not found")
        return product


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = "slug"


    def get_queryset(self):
        return Category.objects.filter(is_active=True).language(self.request.query_params.get("lang", "uz"))

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        products = Product.objects.filter(category=category, is_active=True).language(self.request.query_params.get("lang", "uz"))
        page = self.paginate_queryset(products)

        if page is not None:
            serializer = ProductSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = "name"

    def get_queryset(self):
        # return Manufacturer.objects.all().language(self.request.query_params.get("lang", "uz"))
        pass
        # Нужно получить всех производителей, которые есть в продуктах определенной категории
        category = self.request.query_params.get("category")
        if not category:
            return Manufacturer.objects.all().language(self.request.query_params.get("lang", "uz"))
        return Manufacturer.objects.filter(
            product__category__slug=category
        ).distinct().language(self.request.query_params.get("lang", "uz"))


