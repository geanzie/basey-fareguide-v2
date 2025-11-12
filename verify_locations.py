"""Quick verification of database locations"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bfg.settings')
django.setup()

from locations.models import Location, LocationType

print("=" * 60)
print("DATABASE LOCATIONS SUMMARY")
print("=" * 60)
print(f"\nTotal Locations: {Location.objects.count()}")
print(f"\nBreakdown:")
print(f"  Barangays: {Location.objects.filter(type=LocationType.BARANGAY).count()}")
print(f"  Landmarks: {Location.objects.filter(type=LocationType.LANDMARK).count()}")
print(f"  Sitios: {Location.objects.filter(type=LocationType.SITIO).count()}")
print(f"  Poblacion: {Location.objects.filter(type=LocationType.POBLACION).count()}")

print(f"\nSample Barangays:")
for loc in Location.objects.filter(type=LocationType.BARANGAY)[:5]:
    print(f"  - {loc.name} ({loc.latitude}, {loc.longitude})")

print(f"\nSample Landmarks:")
for loc in Location.objects.filter(type=LocationType.LANDMARK)[:5]:
    print(f"  - {loc.name}")

print("\n" + "=" * 60)
