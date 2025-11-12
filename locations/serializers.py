from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model"""
    coordinates = serializers.ReadOnlyField()
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'type', 'description', 'latitude', 'longitude',
            'barangay', 'boundary_data', 'is_active', 'created_at',
            'updated_at', 'coordinates'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LocationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for location lists"""
    coordinates = serializers.ReadOnlyField()
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'type', 'barangay', 'latitude', 'longitude', 'coordinates', 'is_active']
