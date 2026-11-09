from django.urls import path
from catalog.api.luxury_special import LuxurySpecialListView
from catalog.api.products import ProductDetailView, ProductListView
from catalog.api.wishlist import WishlistView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('luxury-special/', LuxurySpecialListView.as_view(), name='luxury-special'),
    path('me/wishlist/', WishlistView.as_view(), name='my-wishlist'),
]
