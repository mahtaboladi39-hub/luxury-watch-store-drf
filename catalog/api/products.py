from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from catalog.models import Product
from catalog.serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.select_related('brand', 'category').all()


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    queryset = Product.objects.select_related('brand', 'category').prefetch_related(
        'images', 'colors', 'comments__customer__user'
    )

    def get_object(self):
        # Atomic increment in a single UPDATE; annotate() cannot persist values.
        updated = Product.objects.filter(slug=self.kwargs['slug']).update(
            click_count=F('click_count') + 1
        )
        if not updated:
            raise Http404
        return get_object_or_404(self.get_queryset(), slug=self.kwargs['slug'])
