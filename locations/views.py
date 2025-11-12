from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Location
from .serializers import LocationSerializer, LocationListSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for Location model"""
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]  # Locations are public
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'barangay', 'is_active']
    search_fields = ['name', 'barangay', 'description']
    ordering_fields = ['name', 'type', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Use simplified serializer for list view"""
        if self.action == 'list':
            return LocationListSerializer
        return LocationSerializer
