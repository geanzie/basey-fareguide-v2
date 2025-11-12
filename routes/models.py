from django.db import models
from locations.models import Location

class TransportType(models.TextChoices):
    TRICYCLE = 'TRICYCLE', 'Tricycle'
    JEEPNEY = 'JEEPNEY', 'Jeepney'
    MOTORCYCLE = 'MOTORCYCLE', 'Motorcycle'
    VAN = 'VAN', 'Van'
    BOAT = 'BOAT', 'Boat'

class Route(models.Model):
    """Represents a transportation route between two locations"""
    origin = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        related_name='routes_from'
    )
    destination = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        related_name='routes_to'
    )
    transport_type = models.CharField(
        max_length=20, 
        choices=TransportType.choices
    )
    distance_km = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    estimated_duration_minutes = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['origin', 'destination']
        unique_together = ['origin', 'destination', 'transport_type']
        
    def __str__(self):
        return f"{self.origin} to {self.destination} ({self.get_transport_type_display()})"
