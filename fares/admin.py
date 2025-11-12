from django.contrib import admin
from .models import Fare


@admin.register(Fare)
class FareAdmin(admin.ModelAdmin):
    """Admin for Fare model"""
    list_display = [
        'route', 'passenger_type', 'amount',
        'effective_date', 'expiry_date', 'is_active', 'created_at'
    ]
    list_filter = ['passenger_type', 'is_active', 'effective_date']
    search_fields = ['route__origin__name', 'route__destination__name', 'notes']
    ordering = ['-effective_date']
    raw_id_fields = ['route']
    readonly_fields = ['created_at', 'updated_at']
