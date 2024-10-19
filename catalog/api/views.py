from django.db.models import Q, Case, When, Value, IntegerField
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from catalog.api.serializers import ProductSerializer, CategorySerializer
from catalog.models import Product, Category


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = "slug"

    def get_queryset(self):
        search_query = self.request.query_params.get("search", "")
        lang = self.request.query_params.get("lang", "uz")
        queryset = Product.objects.filter(is_active=True).language(lang)

        if search_query:
            queryset = (
                queryset.filter(
                    Q(translations__name__icontains=search_query)
                    | Q(translations__description__icontains=search_query)
                )
                .annotate(
                    relevance=(
                        Case(
                            When(
                                translations__name__icontains=search_query,
                                then=Value(2),
                            ),
                            default=Value(0),
                            output_field=IntegerField(),
                        )
                        + Case(
                            When(
                                translations__description__icontains=search_query,
                                then=Value(1),
                            ),
                            default=Value(0),
                            output_field=IntegerField(),
                        )
                    )
                )
                .order_by("-relevance")
            )

        # Удаление дубликатов по id
        unique_results = []
        seen_ids = set()
        for product in queryset:
            if product.id not in seen_ids:
                unique_results.append(product)
                seen_ids.add(product.id)

        return unique_results

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
        return (
            Category.objects.filter(is_active=True)
            .language(self.request.query_params.get("lang", "uz"))
            .all()
        )

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        products = Product.objects.filter(category=category, is_active=True).language(
            request.query_params.get("lang", "uz")
        )
        page = self.paginate_queryset(products)

        if page is not None:
            serializer = ProductSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)
