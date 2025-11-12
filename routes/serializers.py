from rest_framework import serializers
from .models import Route
from locations.serializers import LocationListSerializer


class RouteSerializer(serializers.ModelSerializer):
    """Serializer for Route model"""
    origin_details = LocationListSerializer(source='origin', read_only=True)
    destination_details = LocationListSerializer(source='destination', read_only=True)
    
    class Meta:
        model = Route
        fields = [
            'id', 'origin', 'origin_details', 'destination', 'destination_details',
            'transport_type', 'distance_km', 'estimated_duration_minutes',
            'is_active', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RouteCalculationSerializer(serializers.Serializer):
    """Serializer for route calculation requests"""
    origin = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2,
        help_text="Origin coordinates [latitude, longitude]"
    )
    destination = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2,
        help_text="Destination coordinates [latitude, longitude]"
    )
    user_id = serializers.IntegerField(required=False, allow_null=True)
    use_google_maps = serializers.BooleanField(default=True)
    passenger_type = serializers.ChoiceField(
        choices=['REGULAR', 'SENIOR', 'PWD', 'STUDENT'],
        default='REGULAR',
        required=False,
        help_text="Passenger type for discount calculation"
    )
