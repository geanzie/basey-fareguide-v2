"""
Script to create sample data for Basey Fare Guide
Populates database with test locations, routes, and sample data

WARNING: This script creates development users with default passwords.
         DO NOT use these credentials in production!
         Change passwords after running in production environment.
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bfg.settings')
django.setup()

from django.contrib.auth import get_user_model
from locations.models import Location, LocationType
from routes.models import Route, TransportType
from fares.models import Fare, PassengerType
from datetime import date, timedelta

User = get_user_model()

def create_sample_locations():
    """Create sample Basey locations"""
    print("Creating sample locations...")
    
    locations_data = [
        # Poblacion Barangays
        {
            'name': 'Baybay (Poblacion)',
            'type': LocationType.POBLACION,
            'latitude': 11.28167,
            'longitude': 125.06833,
            'description': 'Poblacion barangay'
        },
        {
            'name': 'Mercado (Poblacion)',
            'type': LocationType.POBLACION,
            'latitude': 11.2802,
            'longitude': 125.0691,
            'description': 'Market area'
        },
        {
            'name': 'Tinago (Poblacion)',
            'type': LocationType.POBLACION,
            'latitude': 11.2815,
            'longitude': 125.0705,
            'description': 'Poblacion barangay'
        },
        
        # Rural Barangays
        {
            'name': 'Amandayehan',
            'type': LocationType.BARANGAY,
            'latitude': 11.2755464,
            'longitude': 124.9989947,
            'barangay': 'Amandayehan',
            'description': 'Rural barangay'
        },
        {
            'name': 'Bacubac',
            'type': LocationType.BARANGAY,
            'latitude': 11.3012,
            'longitude': 125.0823,
            'barangay': 'Bacubac',
            'description': 'Rural barangay'
        },
        {
            'name': 'Basiao',
            'type': LocationType.BARANGAY,
            'latitude': 11.2768363,
            'longitude': 125.0114879,
            'barangay': 'Basiao',
            'description': 'Coastal barangay'
        },
        
        # Landmarks
        {
            'name': 'José Rizal Monument (Basey Center - KM 0)',
            'type': LocationType.LANDMARK,
            'latitude': 11.28026,
            'longitude': 125.06909,
            'description': 'Central landmark and kilometer zero marker'
        },
        {
            'name': 'Basey Public Market',
            'type': LocationType.LANDMARK,
            'latitude': 11.2803,
            'longitude': 125.0692,
            'description': 'Main public market'
        },
        {
            'name': 'Basey Municipal Hall',
            'type': LocationType.LANDMARK,
            'latitude': 11.2805,
            'longitude': 125.0690,
            'description': 'Municipal government center'
        },
    ]
    
    created = 0
    for loc_data in locations_data:
        location, created_flag = Location.objects.get_or_create(
            name=loc_data['name'],
            defaults=loc_data
        )
        if created_flag:
            created += 1
            print(f"  ✅ Created: {location.name}")
        else:
            print(f"  ℹ️  Exists: {location.name}")
    
    print(f"✅ Created {created} new locations\n")
    return Location.objects.all()


def create_sample_routes(locations):
    """Create sample routes between locations"""
    print("Creating sample routes...")
    
    # Get specific locations
    center = Location.objects.filter(name__contains='Rizal Monument').first()
    basiao = Location.objects.filter(name='Basiao').first()
    bacubac = Location.objects.filter(name='Bacubac').first()
    
    routes_data = []
    
    if center and basiao:
        routes_data.append({
            'origin': center,
            'destination': basiao,
            'transport_type': TransportType.TRICYCLE,
            'distance_km': 5.5,
            'estimated_duration_minutes': 15,
            'notes': 'Coastal route'
        })
    
    if center and bacubac:
        routes_data.append({
            'origin': center,
            'destination': bacubac,
            'transport_type': TransportType.TRICYCLE,
            'distance_km': 3.2,
            'estimated_duration_minutes': 10,
            'notes': 'Short route'
        })
    
    created = 0
    for route_data in routes_data:
        route, created_flag = Route.objects.get_or_create(
            origin=route_data['origin'],
            destination=route_data['destination'],
            transport_type=route_data['transport_type'],
            defaults=route_data
        )
        if created_flag:
            created += 1
            print(f"  ✅ Created: {route}")
        else:
            print(f"  ℹ️  Exists: {route}")
    
    print(f"✅ Created {created} new routes\n")
    return Route.objects.all()


def create_sample_fares(routes):
    """Create sample fare prices for routes"""
    print("Creating sample fares...")
    
    created = 0
    for route in routes:
        # Regular fare
        fare, created_flag = Fare.objects.get_or_create(
            route=route,
            passenger_type=PassengerType.REGULAR,
            defaults={
                'amount': 24.00,
                'effective_date': date.today(),
                'expiry_date': date.today() + timedelta(days=365),
                'notes': 'Standard fare based on Municipal Ordinance 105'
            }
        )
        if created_flag:
            created += 1
            print(f"  ✅ Created: {fare}")
        
        # Senior citizen fare (20% discount)
        fare_senior, created_flag = Fare.objects.get_or_create(
            route=route,
            passenger_type=PassengerType.SENIOR,
            defaults={
                'amount': 19.20,
                'effective_date': date.today(),
                'expiry_date': date.today() + timedelta(days=365),
                'notes': '20% discount for senior citizens'
            }
        )
        if created_flag:
            created += 1
    
    print(f"✅ Created {created} new fares\n")


def create_admin_user():
    """Create admin user if doesn't exist"""
    print("Creating admin user...")
    
    admin_username = 'admin'
    admin_email = 'admin@baseyfareguide.com'
    admin_password = 'admin123'
    
    if User.objects.filter(username=admin_username).exists():
        print(f"  ℹ️  Admin user '{admin_username}' already exists\n")
        return User.objects.get(username=admin_username)
    
    admin = User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        first_name='Admin',
        last_name='User',
        role='ADMIN'
    )
    
    print(f"  ✅ Created admin user:")
    print(f"     Username: {admin_username}")
    print(f"     Password: {admin_password}")
    print(f"     Email: {admin_email}\n")
    
    return admin


def create_test_user():
    """Create test public user"""
    print("Creating test user...")
    
    test_username = 'testuser'
    test_email = 'test@baseyfareguide.com'
    test_password = 'test123'
    
    if User.objects.filter(username=test_username).exists():
        print(f"  ℹ️  Test user '{test_username}' already exists\n")
        return User.objects.get(username=test_username)
    
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password,
        first_name='Test',
        last_name='User',
        role='PUBLIC_USER'
    )
    
    print(f"  ✅ Created test user:")
    print(f"     Username: {test_username}")
    print(f"     Password: {test_password}")
    print(f"     Email: {test_email}\n")
    
    return user


def main():
    """Main function to populate database"""
    print("=" * 60)
    print("🚀 BASEY FARE GUIDE - DATABASE SETUP")
    print("=" * 60)
    print()
    
    # Create users
    admin = create_admin_user()
    user = create_test_user()
    
    # Create locations
    locations = create_sample_locations()
    
    # Create routes
    routes = create_sample_routes(locations)
    
    # Create fares
    create_sample_fares(routes)
    
    print("=" * 60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("📊 Summary:")
    print(f"   Users: {User.objects.count()}")
    print(f"   Locations: {Location.objects.count()}")
    print(f"   Routes: {Route.objects.count()}")
    print(f"   Fares: {Fare.objects.count()}")
    print()
    print("🌐 Next steps:")
    print("   1. Start server: python manage.py runserver")
    print("   2. Admin panel: http://localhost:8000/admin/")
    print("   3. API docs: http://localhost:8000/api/")
    print()
    print("🔐 Login credentials:")
    print("   Admin: admin / admin123")
    print("   User:  testuser / test123")
    print()


if __name__ == '__main__':
    main()
