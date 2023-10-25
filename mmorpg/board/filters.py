from django_filters import FilterSet
from .models import Response

# создаём фильтр
class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
                    'responseUser__username': ['icontains'],
                    'responsePost__title': ['icontains'],
                    'text': ['icontains'],
                    'accepted': ['exact'],
                }