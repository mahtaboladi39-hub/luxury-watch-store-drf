from django.urls import path
from catalog.api.views import ProductListView, ProductDetailView, LuxurySpecialListView, WishlistView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('luxury-special/', LuxurySpecialListView.as_view(), name='luxury-special'),
    path('me/wishlist/', WishlistView.as_view(), name='my-wishlist'),
]
