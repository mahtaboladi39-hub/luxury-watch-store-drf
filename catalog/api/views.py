from django.db.models import Avg, F, Subquery
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from catalog.models import Product, WishList
from catalog.serializers import ProductDetailSerializer, ProductListSerializer, LuxuryProductSerializer, WishlistSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.select_related('brand', 'category').all()


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    def get_object(self):
        Product.objects.filter(slug=self.kwargs['slug']).update(click_count=F('click_count') + 1)
        return get_object_or_404(
            Product.objects.select_related('brand', 'category')
            .prefetch_related('images', 'colors', 'comments__customer__user'),
            slug=self.kwargs['slug'],
        )


class LuxurySpecialListView(ListAPIView):
    serializer_class = LuxuryProductSerializer
    queryset = Product.objects.filter(is_special=True, is_luxury=True, is_available=True).annotate(
        average_luxury_price=Subquery(Product.objects.filter(is_luxury=True).order_by().values('is_luxury').annotate(value=Avg('price')).values('value')[:1])
    ).select_related('brand', 'category')


class WishlistView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return WishList.objects.filter(customer__user=self.request.user).select_related(
            'product', 'customer__user'
        ).order_by('-created_at')

