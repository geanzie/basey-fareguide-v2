from django.db import models


class LocationType(models.TextChoices):
    BARANGAY = 'BARANGAY', 'Barangay'
    LANDMARK = 'LANDMARK', 'Landmark'
    SITIO = 'SITIO', 'Sitio'
    POBLACION = 'POBLACION', 'Poblacion'


class Location(models.Model):
    """Represents a location/destination in Basey"""
    name = models.CharField(max_length=200, unique=True, db_index=True)
    type = models.CharField(
        max_length=20,
        choices=LocationType.choices,
        default=LocationType.BARANGAY,
        db_index=True
    )
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    barangay = models.CharField(max_length=200, blank=True, null=True)
    
    # GeoJSON data for boundary polygons (for barangays)
    boundary_data = models.JSONField(null=True, blank=True, help_text="GeoJSON polygon coordinates")
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['type', 'is_active']),
            models.Index(fields=['barangay']),
        ]
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
    @property
    def coordinates(self):
        """Returns coordinates as dict for JSON serialization"""
        if self.latitude and self.longitude:
            return {
                'lat': float(self.latitude),
                'lng': float(self.longitude)
            }
        return None
