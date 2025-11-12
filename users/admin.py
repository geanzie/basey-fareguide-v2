from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import (
    User, Vehicle, DiscountCard, DiscountUsageLog,
    Incident, FareCalculation
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'email')}),
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Admin for Vehicle model"""
    list_display = ['plate_number', 'vehicle_type', 'owner', 'color', 'is_active', 'created_at']
    list_filter = ['vehicle_type', 'is_active', 'created_at']
    search_fields = ['plate_number', 'owner__username', 'model', 'color']
    ordering = ['-created_at']
    raw_id_fields = ['owner']


@admin.register(DiscountCard)
class DiscountCardAdmin(admin.ModelAdmin):
    """Admin for DiscountCard model"""
    list_display = [
        'id_number', 'user', 'discount_type', 'verification_badge',
        'is_active', 'valid_from', 'valid_until', 'usage_count'
    ]
    list_filter = ['discount_type', 'verification_status', 'is_active', 'created_at']
    search_fields = ['id_number', 'user__username', 'user__email']
    ordering = ['-created_at']
    raw_id_fields = ['user', 'verified_by']
    readonly_fields = ['verified_at', 'last_used_at', 'usage_count', 'daily_usage_count']
    
    fieldsets = (
        ('Card Information', {
            'fields': ('user', 'discount_type', 'id_number', 'id_image', 'discount_rate')
        }),
        ('Verification', {
            'fields': ('verification_status', 'verification_notes', 'verified_at', 'verified_by')
        }),
        ('Validity', {
            'fields': ('is_active', 'valid_from', 'valid_until')
        }),
        ('Usage Statistics', {
            'fields': ('last_used_at', 'usage_count', 'daily_usage_count')
        }),
    )
    
    def verification_badge(self, obj):
        """Colored badge for verification status"""
        colors = {
            'PENDING': 'orange',
            'APPROVED': 'green',
            'REJECTED': 'red'
        }
        color = colors.get(obj.verification_status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_verification_status_display()
        )
    verification_badge.short_description = 'Status'
    
    actions = ['approve_cards', 'reject_cards']
    
    def approve_cards(self, request, queryset):
        """Approve selected discount cards"""
        from django.utils import timezone
        updated = queryset.update(
            verification_status='APPROVED',
            verified_at=timezone.now(),
            verified_by=request.user
        )
        self.message_user(request, f'{updated} card(s) approved.')
    approve_cards.short_description = 'Approve selected cards'
    
    def reject_cards(self, request, queryset):
        """Reject selected discount cards"""
        from django.utils import timezone
        updated = queryset.update(
            verification_status='REJECTED',
            verified_at=timezone.now(),
            verified_by=request.user
        )
        self.message_user(request, f'{updated} card(s) rejected.')
    reject_cards.short_description = 'Reject selected cards'


@admin.register(DiscountUsageLog)
class DiscountUsageLogAdmin(admin.ModelAdmin):
    """Admin for DiscountUsageLog model"""
    list_display = [
        'discount_card', 'used_amount', 'original_fare',
        'discounted_fare', 'from_location', 'to_location', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['discount_card__id_number', 'from_location', 'to_location']
    ordering = ['-created_at']
    raw_id_fields = ['discount_card']
    readonly_fields = ['created_at']


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    """Admin for Incident model"""
    list_display = [
        'id', 'incident_type', 'user', 'status_badge',
        'priority_badge', 'location', 'created_at'
    ]
    list_filter = ['incident_type', 'status', 'priority', 'created_at']
    search_fields = ['description', 'location', 'user__username']
    ordering = ['-created_at']
    raw_id_fields = ['user', 'resolved_by']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    
    fieldsets = (
        ('Incident Details', {
            'fields': ('user', 'incident_type', 'description', 'location', 'gps_coordinates')
        }),
        ('Vehicle Information', {
            'fields': ('vehicle_info',)
        }),
        ('Evidence', {
            'fields': ('evidence_files',)
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'admin_notes')
        }),
        ('Resolution', {
            'fields': ('resolved_at', 'resolved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def status_badge(self, obj):
        """Colored badge for status"""
        colors = {
            'PENDING': 'orange',
            'UNDER_REVIEW': 'blue',
            'RESOLVED': 'green',
            'DISMISSED': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        """Colored badge for priority"""
        colors = {
            'LOW': 'green',
            'MEDIUM': 'orange',
            'HIGH': 'red',
            'CRITICAL': 'darkred'
        }
        color = colors.get(obj.priority, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'


@admin.register(FareCalculation)
class FareCalculationAdmin(admin.ModelAdmin):
    """Admin for FareCalculation model"""
    list_display = [
        'id', 'user', 'from_location', 'to_location',
        'distance', 'calculated_fare', 'discount_applied',
        'calculation_type', 'created_at'
    ]
    list_filter = ['calculation_type', 'created_at']
    search_fields = ['from_location', 'to_location', 'user__username']
    ordering = ['-created_at']
    raw_id_fields = ['user', 'vehicle', 'discount_card']
    readonly_fields = ['created_at']
