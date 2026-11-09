from django.db.models import Avg, Subquery
from rest_framework.generics import ListAPIView

from catalog.models import Product
from catalog.serializers import LuxuryProductSerializer


class LuxurySpecialListView(ListAPIView):
    serializer_class = LuxuryProductSerializer
    queryset = Product.objects.filter(
        is_special=True,
        is_luxury=True,
        is_available=True,
    ).annotate(
        average_luxury_price=Subquery(
            Product.objects.filter(is_luxury=True)
            .order_by()
            .values('is_luxury')
            .annotate(value=Avg('price'))
            .values('value')[:1]
        )
    )
