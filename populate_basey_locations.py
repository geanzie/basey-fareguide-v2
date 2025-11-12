"""
Script to populate database with Basey locations from basey-locations.json
Imports all barangays, landmarks, and sitios with coordinates
"""
import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bfg.settings')
django.setup()

from locations.models import Location, LocationType

def load_locations_from_json():
    """Load locations from basey-locations.json file"""
    json_file = 'basey-locations.json'
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        return None
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📄 Loaded {json_file}")
    print(f"   Municipality: {data['metadata']['municipality']}, {data['metadata']['province']}")
    print(f"   Total locations: {data['metadata']['total_locations']}")
    print(f"   Last updated: {data['metadata']['last_updated']}")
    print()
    
    return data

def populate_barangays(barangays_data):
    """Populate barangay locations"""
    print("📍 Populating Barangays...")
    created = 0
    updated = 0
    
    for barangay in barangays_data:
        location, created_flag = Location.objects.update_or_create(
            name=barangay['name'],
            type=LocationType.BARANGAY,
            defaults={
                'latitude': barangay['coordinates']['lat'],
                'longitude': barangay['coordinates']['lng'],
                'barangay': barangay['name'],
                'description': f"{barangay.get('address', '')} (Source: {barangay.get('source', 'unknown')})",
                'is_active': True
            }
        )
        
        if created_flag:
            created += 1
            print(f"  ✅ Created: {location.name}")
        else:
            updated += 1
            print(f"  🔄 Updated: {location.name}")
    
    print(f"✅ Barangays - Created: {created}, Updated: {updated}\n")
    return created, updated

def populate_landmarks(landmarks_data):
    """Populate landmark locations"""
    print("🏛️ Populating Landmarks...")
    created = 0
    updated = 0
    
    for landmark in landmarks_data:
        location, created_flag = Location.objects.update_or_create(
            name=landmark['name'],
            type=LocationType.LANDMARK,
            defaults={
                'latitude': landmark['coordinates']['lat'],
                'longitude': landmark['coordinates']['lng'],
                'description': f"{landmark.get('address', '')} (Source: {landmark.get('source', 'unknown')})",
                'is_active': True
            }
        )
        
        if created_flag:
            created += 1
            print(f"  ✅ Created: {location.name}")
        else:
            updated += 1
            print(f"  🔄 Updated: {location.name}")
    
    print(f"✅ Landmarks - Created: {created}, Updated: {updated}\n")
    return created, updated

def populate_sitios(sitios_data):
    """Populate sitio locations"""
    print("🏘️ Populating Sitios...")
    created = 0
    updated = 0
    
    for sitio in sitios_data:
        location, created_flag = Location.objects.update_or_create(
            name=sitio['name'],
            type=LocationType.SITIO,
            defaults={
                'latitude': sitio['coordinates']['lat'],
                'longitude': sitio['coordinates']['lng'],
                'description': f"{sitio.get('address', '')} (Source: {sitio.get('source', 'unknown')})",
                'is_active': True
            }
        )
        
        if created_flag:
            created += 1
            print(f"  ✅ Created: {location.name}")
        else:
            updated += 1
            print(f"  🔄 Updated: {location.name}")
    
    print(f"✅ Sitios - Created: {created}, Updated: {updated}\n")
    return created, updated

def main():
    """Main function to populate all locations"""
    print("=" * 70)
    print("🗺️  BASEY FARE GUIDE - LOCATIONS DATABASE POPULATION")
    print("=" * 70)
    print()
    
    # Load JSON data
    data = load_locations_from_json()
    if not data:
        return
    
    # Track statistics
    total_created = 0
    total_updated = 0
    
    # Populate barangays
    if 'barangay' in data['locations']:
        created, updated = populate_barangays(data['locations']['barangay'])
        total_created += created
        total_updated += updated
    
    # Populate landmarks
    if 'landmark' in data['locations']:
        created, updated = populate_landmarks(data['locations']['landmark'])
        total_created += created
        total_updated += updated
    
    # Populate sitios
    if 'sitio' in data['locations']:
        created, updated = populate_sitios(data['locations']['sitio'])
        total_created += created
        total_updated += updated
    
    print("=" * 70)
    print("✅ LOCATION POPULATION COMPLETE!")
    print("=" * 70)
    print()
    print("📊 Summary:")
    print(f"   Total Locations in Database: {Location.objects.count()}")
    print(f"   New Locations Created: {total_created}")
    print(f"   Existing Locations Updated: {total_updated}")
    print()
    print("📍 Breakdown by Type:")
    print(f"   Barangays: {Location.objects.filter(type=LocationType.BARANGAY).count()}")
    print(f"   Landmarks: {Location.objects.filter(type=LocationType.LANDMARK).count()}")
    print(f"   Sitios: {Location.objects.filter(type=LocationType.SITIO).count()}")
    print(f"   Poblacion: {Location.objects.filter(type=LocationType.POBLACION).count()}")
    print()
    print("🌐 Next steps:")
    print("   1. Start server: python manage.py runserver")
    print("   2. View locations: http://localhost:8000/api/locations/")
    print("   3. Admin panel: http://localhost:8000/admin/locations/location/")
    print()

if __name__ == '__main__':
    main()
