"""
Generate comprehensive routes and fares for all locations in Basey
This creates routes between Basey Center (KM 0) and all barangays
"""
import os
import django
from math import radians, cos, sin, asin, sqrt

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bfg.settings')
django.setup()

from locations.models import Location, LocationType
from routes.models import Route, TransportType
from fares.models import Fare, PassengerType


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


def calculate_fare(distance_km):
    """
    Calculate fare based on distance using Basey fare matrix
    Base fare: ₱15 for first 2km
    Additional: ₱2 per km after that
    """
    if distance_km <= 2:
        return 15.0
    else:
        additional_km = distance_km - 2
        return 15.0 + (additional_km * 2.0)


def estimate_duration(distance_km, transport_type):
    """Estimate travel duration based on distance and transport type"""
    # Average speeds in km/h
    speeds = {
        TransportType.TRICYCLE: 25,  # 25 km/h average
        TransportType.JEEPNEY: 30,   # 30 km/h average
        TransportType.MOTORCYCLE: 35, # 35 km/h average
        TransportType.HABAL_HABAL: 30, # 30 km/h average
        TransportType.VAN: 40,       # 40 km/h average
        TransportType.BOAT: 20,      # 20 km/h average
    }
    
    speed = speeds.get(transport_type, 25)
    duration_hours = distance_km / speed
    duration_minutes = int(duration_hours * 60)
    
    return max(5, duration_minutes)  # Minimum 5 minutes


def generate_routes_and_fares():
    """Generate routes and fares from Basey Center to all barangays"""
    print("=" * 70)
    print("🚀 GENERATING COMPREHENSIVE ROUTES AND FARES")
    print("=" * 70)
    print()
    
    # Get Basey Center (KM 0) as the main hub
    center = Location.objects.filter(name__icontains='Rizal Monument').first()
    
    if not center:
        # Fallback to any landmark in poblacion
        center = Location.objects.filter(type=LocationType.LANDMARK).first()
    
    if not center:
        print("❌ Error: No center location found!")
        return
    
    print(f"📍 Hub Location: {center.name}")
    print(f"   Coordinates: {center.latitude}, {center.longitude}")
    print()
    
    # Get all barangays and other locations (excluding the center itself)
    destinations = Location.objects.exclude(id=center.id).order_by('name')
    
    print(f"📊 Found {destinations.count()} potential destinations")
    print()
    
    routes_created = 0
    fares_created = 0
    routes_skipped = 0
    
    for destination in destinations:
        # Skip if both locations don't have coordinates
        if not all([center.latitude, center.longitude, 
                   destination.latitude, destination.longitude]):
            print(f"  ⚠️  Skipping {destination.name} - missing coordinates")
            routes_skipped += 1
            continue
        
        # Calculate distance
        distance = calculate_distance(
            center.latitude, center.longitude,
            destination.latitude, destination.longitude
        )
        
        # Round to 1 decimal place
        distance = round(distance, 1)
        
        # Determine transport type based on distance and location type
        if distance <= 3:
            transport_type = TransportType.TRICYCLE
        elif distance <= 10:
            transport_type = TransportType.TRICYCLE  # Still tricycle for medium distances
        else:
            transport_type = TransportType.JEEPNEY  # Jeepney for longer distances
        
        # Calculate duration
        duration = estimate_duration(distance, transport_type)
        
        # Create route (both directions)
        for origin, dest in [(center, destination), (destination, center)]:
            route, created = Route.objects.get_or_create(
                origin=origin,
                destination=dest,
                transport_type=transport_type,
                defaults={
                    'distance_km': distance,
                    'estimated_duration_minutes': duration,
                    'is_active': True,
                    'notes': f'Auto-generated route'
                }
            )
            
            if created:
                routes_created += 1
                
                # Calculate fare
                base_fare = calculate_fare(distance)
                
                # Create fares for different passenger types
                from datetime import date
                
                fare_types = [
                    (PassengerType.REGULAR, base_fare),
                    (PassengerType.STUDENT, base_fare * 0.8),  # 20% discount
                    (PassengerType.SENIOR, base_fare * 0.8),   # 20% discount
                    (PassengerType.PWD, base_fare * 0.8),      # 20% discount
                ]
                
                for pax_type, fare_amount in fare_types:
                    fare, fare_created = Fare.objects.get_or_create(
                        route=route,
                        passenger_type=pax_type,
                        defaults={
                            'amount': round(fare_amount, 2),
                            'effective_date': date.today(),
                            'is_active': True,
                            'notes': 'Auto-generated fare'
                        }
                    )
                    
                    if fare_created:
                        fares_created += 1
        
        # Print progress every 10 locations
        if (routes_created // 2) % 10 == 0 and routes_created > 0:
            print(f"  ✓ Processed {routes_created // 2} locations...")
    
    print()
    print("=" * 70)
    print("✅ ROUTE AND FARE GENERATION COMPLETE!")
    print("=" * 70)
    print()
    print("📊 Summary:")
    print(f"   Routes created: {routes_created}")
    print(f"   Fares created: {fares_created}")
    print(f"   Routes skipped: {routes_skipped}")
    print()
    print("📈 Database Totals:")
    print(f"   Total Locations: {Location.objects.count()}")
    print(f"   Total Routes: {Route.objects.count()}")
    print(f"   Total Fares: {Fare.objects.count()}")
    print()
    print("🌐 Test your API:")
    print(f"   Routes: /v2/routes/")
    print(f"   Fares: /v2/fares/")
    print(f"   Calculate: /v2/routes/calculate/?origin=1&destination=2")
    print()


if __name__ == '__main__':
    generate_routes_and_fares()
