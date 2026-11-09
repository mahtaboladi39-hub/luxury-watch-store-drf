from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView

from catalog.models import Product
from catalog.serializers import ProductDetailSerializer, ProductListSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.select_related('brand', 'category').all()


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        Product.objects.filter(slug=self.kwargs['slug']).update(
            click_count=F('click_count') + 1
        )
        return get_object_or_404(
            Product.objects.select_related('brand', 'category').prefetch_related(
                'images', 'colors', 'comments__customer__user'
            ),
            slug=self.kwargs['slug'],
        )
