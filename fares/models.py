from django.db import models
from routes.models import Route

class PassengerType(models.TextChoices):
    REGULAR = 'REGULAR', 'Regular'
    STUDENT = 'STUDENT', 'Student'
    SENIOR = 'SENIOR', 'Senior Citizen'
    PWD = 'PWD', 'Person with Disability'
    CHILD = 'CHILD', 'Child'

class Fare(models.Model):
    """Represents fare information for a specific route"""
    route = models.ForeignKey(
        Route, 
        on_delete=models.CASCADE, 
        related_name='fares'
    )
    passenger_type = models.CharField(
        max_length=20, 
        choices=PassengerType.choices,
        default=PassengerType.REGULAR
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-effective_date', 'passenger_type']
        
    def __str__(self):
        return f"{self.route} - ₱{self.amount} ({self.get_passenger_type_display()})"
