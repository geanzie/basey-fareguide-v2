from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Vehicle, DiscountCard, DiscountUsageLog,
    Incident, FareCalculation
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'role', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Create user with hashed password"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user, handling password separately"""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserPublicSerializer(serializers.ModelSerializer):
    """Public user info (limited fields)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']


class VehicleSerializer(serializers.ModelSerializer):
    """Serializer for Vehicle model"""
    owner_details = UserPublicSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'owner', 'owner_details', 'plate_number', 'vehicle_type',
            'model', 'color', 'is_active', 'registration_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DiscountCardSerializer(serializers.ModelSerializer):
    """Serializer for DiscountCard model"""
    user_details = UserPublicSerializer(source='user', read_only=True)
    is_currently_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = DiscountCard
        fields = [
            'id', 'user', 'user_details', 'discount_type', 'id_number',
            'id_image', 'verification_status', 'verification_notes',
            'verified_at', 'verified_by', 'discount_rate', 'is_active',
            'valid_from', 'valid_until', 'last_used_at', 'usage_count',
            'daily_usage_count', 'created_at', 'updated_at', 'is_currently_valid'
        ]
        read_only_fields = [
            'id', 'verification_status', 'verification_notes',
            'verified_at', 'verified_by', 'last_used_at',
            'usage_count', 'daily_usage_count', 'created_at', 'updated_at'
        ]
    
    def get_is_currently_valid(self, obj):
        """Check if card is currently valid"""
        return obj.is_valid()


class DiscountCardVerificationSerializer(serializers.Serializer):
    """Serializer for verifying discount cards (admin only)"""
    action = serializers.ChoiceField(choices=['approve', 'reject'], required=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class DiscountUsageLogSerializer(serializers.ModelSerializer):
    """Serializer for DiscountUsageLog model"""
    discount_card_details = DiscountCardSerializer(source='discount_card', read_only=True)
    
    class Meta:
        model = DiscountUsageLog
        fields = [
            'id', 'discount_card', 'discount_card_details', 'used_amount',
            'original_fare', 'discounted_fare', 'discount_rate',
            'from_location', 'to_location', 'distance', 'ip_address',
            'gps_coordinates', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class IncidentSerializer(serializers.ModelSerializer):
    """Serializer for Incident model"""
    user_details = UserPublicSerializer(source='user', read_only=True)
    resolved_by_details = UserPublicSerializer(source='resolved_by', read_only=True)
    
    class Meta:
        model = Incident
        fields = [
            'id', 'user', 'user_details', 'incident_type', 'description',
            'location', 'gps_coordinates', 'vehicle_info', 'evidence_files',
            'status', 'priority', 'admin_notes', 'resolved_at',
            'resolved_by', 'resolved_by_details', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'resolved_at', 'resolved_by', 'created_at', 'updated_at'
        ]


class IncidentUpdateSerializer(serializers.Serializer):
    """Serializer for updating incident status (admin only)"""
    status = serializers.ChoiceField(
        choices=['PENDING', 'UNDER_REVIEW', 'RESOLVED', 'DISMISSED'],
        required=False
    )
    priority = serializers.ChoiceField(
        choices=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        required=False
    )
    admin_notes = serializers.CharField(required=False, allow_blank=True)


class FareCalculationSerializer(serializers.ModelSerializer):
    """Serializer for FareCalculation model"""
    user_details = UserPublicSerializer(source='user', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    discount_card_details = DiscountCardSerializer(source='discount_card', read_only=True)
    
    class Meta:
        model = FareCalculation
        fields = [
            'id', 'user', 'user_details', 'vehicle', 'vehicle_details',
            'from_location', 'to_location', 'distance', 'calculated_fare',
            'actual_fare', 'original_fare', 'discount_applied', 'discount_type',
            'discount_card', 'discount_card_details', 'calculation_type',
            'route_data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
