from rest_framework import serializers
from .models import Fare
from routes.serializers import RouteSerializer


class FareSerializer(serializers.ModelSerializer):
    """Serializer for Fare model"""
    route_details = RouteSerializer(source='route', read_only=True)
    
    class Meta:
        model = Fare
        fields = [
            'id', 'route', 'route_details', 'passenger_type', 'amount',
            'effective_date', 'expiry_date', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
