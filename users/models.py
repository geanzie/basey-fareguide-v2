from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    MODERATOR = 'MODERATOR', 'Moderator'
    DRIVER = 'DRIVER', 'Driver'
    PUBLIC_USER = 'PUBLIC_USER', 'Public User'


class User(AbstractUser):
    """Extended user model for Basey Fare Guide"""
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PUBLIC_USER,
        db_index=True
    )
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    # Override to make email required
    email = models.EmailField(unique=True)
    
    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['role', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Vehicle(models.Model):
    """Vehicle information for drivers"""
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    plate_number = models.CharField(max_length=20, unique=True, db_index=True)
    vehicle_type = models.CharField(max_length=50)
    model = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    registration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.plate_number} - {self.vehicle_type}"


class DiscountType(models.TextChoices):
    SENIOR_CITIZEN = 'SENIOR_CITIZEN', 'Senior Citizen'
    PWD = 'PWD', 'Person with Disability'
    STUDENT = 'STUDENT', 'Student'


class VerificationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class DiscountCard(models.Model):
    """Discount cards for eligible users (20% discount)"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discount_cards'
    )
    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        db_index=True
    )
    id_number = models.CharField(max_length=100, unique=True, db_index=True)
    id_image = models.ImageField(upload_to='discount_cards/', help_text="Upload ID image")
    
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True
    )
    verification_notes = models.TextField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_discount_cards'
    )
    
    discount_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.20,
        help_text="0.20 for 20% discount"
    )
    
    is_active = models.BooleanField(default=True, db_index=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    
    # Usage tracking
    last_used_at = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    daily_usage_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'verification_status']),
            models.Index(fields=['is_active', 'verification_status']),
            models.Index(fields=['valid_from', 'valid_until']),
        ]
        
    def __str__(self):
        return f"{self.user.username} - {self.get_discount_type_display()} ({self.get_verification_status_display()})"
    
    def is_valid(self):
        """Check if card is currently valid"""
        from django.utils import timezone
        now = timezone.now().date()
        return (
            self.is_active and
            self.verification_status == VerificationStatus.APPROVED and
            self.valid_from <= now <= self.valid_until
        )


class DiscountUsageLog(models.Model):
    """Log every time a discount is used"""
    discount_card = models.ForeignKey(
        DiscountCard,
        on_delete=models.CASCADE,
        related_name='usage_logs'
    )
    used_amount = models.DecimalField(max_digits=8, decimal_places=2)
    original_fare = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_fare = models.DecimalField(max_digits=8, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=4, decimal_places=2)
    
    from_location = models.CharField(max_length=200)
    to_location = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=8, decimal_places=2, help_text="Distance in kilometers")
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    gps_coordinates = models.JSONField(null=True, blank=True, help_text="GPS coordinates {lat, lng}")
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['discount_card', 'created_at']),
        ]
        
    def __str__(self):
        return f"{self.discount_card.user.username} - ₱{self.used_amount} saved"


class IncidentType(models.TextChoices):
    OVERCHARGING = 'OVERCHARGING', 'Overcharging'
    REFUSAL_TO_CONVEY = 'REFUSAL_TO_CONVEY', 'Refusal to Convey'
    RECKLESS_DRIVING = 'RECKLESS_DRIVING', 'Reckless Driving'
    VEHICLE_DEFECT = 'VEHICLE_DEFECT', 'Vehicle Defect'
    OTHER = 'OTHER', 'Other'


class IncidentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    RESOLVED = 'RESOLVED', 'Resolved'
    DISMISSED = 'DISMISSED', 'Dismissed'


class Priority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'


class Incident(models.Model):
    """Incident reporting system"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidents'
    )
    incident_type = models.CharField(
        max_length=30,
        choices=IncidentType.choices,
        db_index=True
    )
    description = models.TextField()
    location = models.CharField(max_length=500)
    gps_coordinates = models.JSONField(null=True, blank=True, help_text="GPS coordinates {lat, lng}")
    
    # Vehicle information
    vehicle_info = models.JSONField(
        null=True,
        blank=True,
        help_text="Vehicle details: plate number, type, color, etc."
    )
    
    # Evidence files (images/videos)
    evidence_files = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of file URLs"
    )
    
    status = models.CharField(
        max_length=20,
        choices=IncidentStatus.choices,
        default=IncidentStatus.PENDING,
        db_index=True
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True
    )
    
    # Admin notes
    admin_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_incidents'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['incident_type', 'status']),
            models.Index(fields=['user', 'created_at']),
        ]
        
    def __str__(self):
        return f"{self.get_incident_type_display()} - {self.get_status_display()}"


class FareCalculation(models.Model):
    """Historical fare calculations"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fare_calculations'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fare_calculations'
    )
    
    from_location = models.CharField(max_length=500)
    to_location = models.CharField(max_length=500)
    
    distance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Distance in kilometers"
    )
    
    calculated_fare = models.DecimalField(max_digits=8, decimal_places=2)
    actual_fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    original_fare = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fare before discount"
    )
    discount_applied = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    discount_type = models.CharField(max_length=50, blank=True)
    discount_card = models.ForeignKey(
        DiscountCard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fare_calculations'
    )
    
    calculation_type = models.CharField(
        max_length=100,
        help_text="Method used: Google Maps Route Planner, GPS, Smart Calculator, etc."
    )
    
    # Detailed route data
    route_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Stores polyline, barangay info, waypoints, etc."
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['calculation_type']),
        ]
        
    def __str__(self):
        return f"{self.from_location} → {self.to_location} - ₱{self.calculated_fare}"
