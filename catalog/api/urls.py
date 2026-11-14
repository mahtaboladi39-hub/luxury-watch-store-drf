from django.urls import path
from catalog.api.luxury_special import LuxurySpecialListView
from catalog.api.products import ProductCreateView, ProductDetailView, ProductListView
from catalog.api.wishlist import WishlistView

urlpatterns = [
    # باید قبل از <slug:slug> بیاید، وگرنه "create" به‌عنوان slug خوانده می‌شود.
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('luxury-special/', LuxurySpecialListView.as_view(), name='luxury-special'),
    path('me/wishlist/', WishlistView.as_view(), name='my-wishlist'),
]
