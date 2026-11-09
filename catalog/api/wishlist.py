from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from catalog.models import WishList
from catalog.serializers import WishlistSerializer


class WishlistView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(customer__user=self.request.user).select_related(
            'product', 'customer__user'
        ).order_by('-created_at')
