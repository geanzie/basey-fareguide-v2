from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Fare
from .serializers import FareSerializer


class FareViewSet(viewsets.ModelViewSet):
    """ViewSet for Fare model"""
    queryset = Fare.objects.filter(is_active=True)
    serializer_class = FareSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['route', 'passenger_type', 'is_active']
