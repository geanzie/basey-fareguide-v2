from django.contrib import admin
from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Admin for Route model"""
    list_display = [
        'origin', 'destination', 'transport_type',
        'distance_km', 'estimated_duration_minutes', 'is_active', 'created_at'
    ]
    list_filter = ['transport_type', 'is_active', 'created_at']
    search_fields = ['origin__name', 'destination__name', 'notes']
    ordering = ['origin', 'destination']
    raw_id_fields = ['origin', 'destination']
    readonly_fields = ['created_at', 'updated_at']
